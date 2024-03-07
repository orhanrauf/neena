from pinecone import Pinecone, PodSpec
from openai import OpenAI
import tiktoken  # TODO: to avoid errors during runtime, use this to count and check no. tokens in input before passing to embedding model
import time
import json

from sqlalchemy.orm import Session
from typing import Any

from app.core.logging import logger
from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.crud_task_definition import task_definition
from app.schemas import TaskDefinition

logger = logger(__name__)


class PineconeClient:
    def __init__(self, api_key: str) -> None:
        self.client = Pinecone(api_key=api_key)


class OpenAIEmbedder:
    def __init__(self) -> None:
        self.client = OpenAI()

    def get_embedding(self, text: str, model="text-embedding-3-small") -> list[float]:
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding


class TaskDefinitionRetriever:
    def __init__(
        self, database_session: Session, pinecone_client: PineconeClient, openai_embedder: OpenAIEmbedder
    ) -> None:
        self.database_session = database_session
        self.pinecone_client = pinecone_client
        self.openai_embedder = openai_embedder
        self.index_name = "task-definitions-te3-small-quickstart"
        self.all_task_definitions = self.get_all_task_definitions()
        self.create_embeddings()
        self.index = self.initialize_index()
        self.populate_vector_database()
        # self.delete_index()

    def retrieve_task_definitions(self, request: str) -> Any:
        chunks = self.get_most_similar_chunks_for_query(query=request)
        return chunks

    def get_all_task_definitions(self) -> list[str]:
        output_task_defintions = []
        all_task_defintions = task_definition.get_multi(db=self.database_session)
        for one_task_definition in all_task_defintions:
            simple_oops = TaskDefinition.model_validate(one_task_definition, from_attributes=True)
            output_task_defintions.append(simple_oops.model_dump_json(indent=2))
        return output_task_defintions

    def initialize_index(self) -> Any:
        existing_indexes = [index_names for index_names in self.pinecone_client.client.list_indexes().names()]

        if self.index_doesnt_exist_yet(existing_indexes):
            self.pinecone_client.client.create_index(
                self.index_name,
                dimension=1536,
                metric="cosine",
                spec=PodSpec(environment="gcp-starter", pod_type="starter"),
            )
            while self.index_not_ready_yet():
                time.sleep(1)
        index = self.pinecone_client.client.Index(self.index_name)
        time.sleep(1)
        print("\nDone initializing index.")
        print(index.describe_index_stats())
        return index

    def index_doesnt_exist_yet(self, existing_indexes: list[str]) -> bool:
        return self.index_name not in existing_indexes

    def index_not_ready_yet(self) -> bool:
        return not self.pinecone_client.client.describe_index(self.index_name).status["ready"]

    def populate_vector_database(self):
        for id, task_definition in enumerate(self.all_task_definitions):
            embedding = self.openai_embedder.get_embedding(text=task_definition)
            task_definition_dict = json.loads(task_definition)
            metadata = {
                "task_name": task_definition_dict["task_name"],
                "description": task_definition_dict["description"],
                "body": task_definition,
            }
            self.index.upsert(vectors=[{"id": str(id), "values": embedding, "metadata": metadata}])
        print("\nDone populating vector index")
        print("\nWaiting 5 seconds...")
        time.sleep(5)
        print(f"\nVector index stats:\n{self.index.describe_index_stats()}")

    def create_embeddings(self) -> None:
        embedding = self.openai_embedder.get_embedding(text=self.all_task_definitions[0])

    def index_embeddings(self) -> None:
        pass

    def get_most_similar_chunks_for_query(self, query: str) -> Any:
        print(f"\nQuery: {query}")
        print("\nEmbedding query using OpenAI ...")
        query_embedding = self.openai_embedder.get_embedding(query)

        print("\nQuerying Pinecone index ...")
        query_results = self.index.query(vector=query_embedding, top_k=3, include_metadata=True)
        context_chunks = [(x["metadata"]["task_name"], x["metadata"]["description"]) for x in query_results["matches"]]
        print(context_chunks)
        return context_chunks

    def delete_index(self) -> None:
        if self.index_name in self.pinecone_client.client.list_indexes().names():
            print("\nDeleting index ...")
            self.pinecone_client.client.delete_index(name=self.index_name)
            print(f"Index {self.index_name} deleted successfully")
        else:
            print("\nNo index to delete!")


_database_session = SessionLocal()
pinecone_client = PineconeClient(settings.PINECONE_API_KEY)
openai_embedder = OpenAIEmbedder()
task_definition_retriever = TaskDefinitionRetriever(
    database_session=_database_session, pinecone_client=pinecone_client, openai_embedder=openai_embedder
)
