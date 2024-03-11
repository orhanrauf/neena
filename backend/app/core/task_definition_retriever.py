import time
import json

from typing import Any
from openai import OpenAI
from sqlalchemy.orm import Session
from pinecone import Pinecone, PodSpec, Index

from app.core.logging import logger
from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.crud_task_definition import task_definition
from app.schemas import TaskDefinition

logger = logger(__name__)


class PineconeService:
    """
    Service class for managing Pinecone vector database operations.

    Attributes:
        client (Pinecone): An instance of the Pinecone client configured with the provided API key.
    """

    def __init__(self, api_key: str) -> None:
        self.client = Pinecone(api_key=api_key)

    def initialize_index(
        self,
        index_name: str,
        dimension: int = 1536,
        similarity_metric: str = "cosine",
        environment: str = "gcp-starter",
        pod_type: str = "starter",
        timeout_threshold: int = 30,
    ) -> Index:
        """
        Main entry point of PineconeService class.
        Initializes a vector index in Pinecone. If the index does not exist, it is created with the specified
        configuration. If the index already exists, the creation step is skipped.

        Args:
            index_name (str): The name of the vector index to be created or verified.
            dimension (int): The dimensionality of the vectors that will be stored in the index.
            similarity_metric (str): The similarity metric to be used for comparing vectors in the index. Common
                                     options include "cosine" for cosine similarity and "euclidean" for Euclidean distance.
            environment (str): The Pinecone environment where the index is deployed, e.g., "gcp-starter".
            pod_type (str): The type of pod to use for the index, e.g., "starter" for starter pods.
            timeout_threshold (int): The maximum number of seconds to wait for the index to be ready. A TimeoutError
                                     is raised if the index is not ready within this time frame.

        Returns:
            Index: An instance of the Pinecone Index class for the specified index name.

        Raises:
            TimeoutError: If the index is not ready within the specified timeout threshold.
        """
        if self._index_does_not_exist(index_name):
            try:
                self.client.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric=similarity_metric,
                    spec=PodSpec(environment=environment, pod_type=pod_type),
                    timeout=timeout_threshold,
                )
                logger.info(
                    f"Successfully created index '{index_name}'. Index stats: {self.client.describe_index(name=index_name)}"
                )
            except TimeoutError as exception:
                raise
        else:
            logger.info(f"Index '{index_name}' already exists. Skipping creation.")
        return self.client.Index(name=index_name)

    def _index_does_not_exist(self, index_name: str) -> bool:
        return index_name not in self.client.list_indexes().names()

    def delete_index(self, index_name: str) -> None:
        if index_name in self.client.list_indexes().names():
            logger.info(f"Deleting index '{index_name}' ...")
            self.client.delete_index(name=index_name)
        else:
            logger.info(f"Index '{index_name}' not found in list of known indexes. No index to delete.")


class OpenAIEmbeddingService:
    """
    Service class for embedding operations using OpenAI.
    """

    def __init__(self, api_key: str = None) -> None:
        self.client = OpenAI(api_key=api_key)

    def get_embedding(self, text: str, model="text-embedding-3-small") -> list[float]:
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding


class TaskDefinitionRetrievalManager:
    """
    Manages the retrieval of task definitions from a vector database based on semantic similarity to user queries. This class
    integrates with Pinecone for vector storage and querying, and utilizes embeddings from OpenAI for semantic understanding.

    Attributes:
        database_session (Session): SQLAlchemy database session for accessing task definitions.
        pinecone_service (PineconeService): Service class for interacting with Pinecone vector databases.
        openai_embedder (OpenAIEmbeddingService): Service class for generating embeddings using OpenAI models.
        index_name (str): Name of the Pinecone vector index used for storing task definition embeddings.
    """

    def __init__(
        self,
        database_session: Session,
        pinecone_service: PineconeService,
        openai_embedder: OpenAIEmbeddingService,
        index_name: str = "task-definitions-te3-small-quickstart",
    ) -> None:
        self.database_session = database_session
        self.pinecone_service = pinecone_service
        self.openai_embedder = openai_embedder
        self.index_name = index_name
        self.all_task_definitions_jsons = self._get_all_task_definition_jsons()
        self.index = self._initialize_index()
        self._populate_vector_database()

    def retrieve_similar_task_definitions(
        self, request: str, top_k: int = 5, include_metadata: bool = True
    ) -> list[TaskDefinition]:
        """
        Main entry point of TaskDefinitionRetriever class.
        Retrieves task definitions that are semantically similar to the given user query.

        Args:
            request (str): User query describing the task flow to generate.
            top_k (int, optional): The number of top similar task definitions to retrieve. Defaults to 5.
            include_metadata (bool, optional): Flag to include metadata in the search results. Defaults to True.

        Returns:
            list[TaskDefinition]: A list of TaskDefinition instances matching the query.
        """
        query_embedding = self.openai_embedder.get_embedding(request)
        search_results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=include_metadata)
        retrieved_task_names = [search_result["metadata"]["task_name"] for search_result in search_results["matches"]]
        return task_definition.get_by_names(self.database_session, retrieved_task_names)

    def _get_all_task_definition_jsons(self) -> list[str]:
        all_task_defintions = task_definition.get_multi(db=self.database_session)
        return [self._get_model_dump_json_from_task_definition(d) for d in all_task_defintions]

    def _get_model_dump_json_from_task_definition(
        self, task_definition: TaskDefinition, json_indent_level: int = 2
    ) -> str:
        return TaskDefinition.model_validate(task_definition, from_attributes=True).model_dump_json(
            indent=json_indent_level
        )

    def _initialize_index(self) -> Index:
        return self.pinecone_service.initialize_index(index_name=self.index_name)

    def _populate_vector_database(self):
        for serialized_task_definition in self.all_task_definitions_jsons:
            embedding = self.openai_embedder.get_embedding(serialized_task_definition)
            task_definition_map = json.loads(serialized_task_definition)
            embedding_metadata = {
                "task_name": task_definition_map["task_name"],
                "description": task_definition_map["description"],
                "serialized_task_description": serialized_task_definition,
            }
            self.index.upsert(
                vectors=[{"id": task_definition_map["id"], "values": embedding, "metadata": embedding_metadata}]
            )


_database_session = SessionLocal()
pinecone_service = PineconeService(settings.PINECONE_API_KEY)
openai_embedder = OpenAIEmbeddingService()
task_definition_retrieval_manager = TaskDefinitionRetrievalManager(
    database_session=_database_session,
    pinecone_service=pinecone_service,
    openai_embedder=openai_embedder,
)
