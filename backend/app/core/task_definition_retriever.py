from pinecone import Pinecone, PodSpec
import langchain
import openai
import tiktoken  # TODO: to avoid errors during runtime, use this to count and check no. tokens in input before passing to embedding model
import time

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.core.config import settings
from app.db.session import SessionLocal
from app.crud.crud_task_definition import task_definition
from app.schemas import TaskDefinition

logger = logger(__name__)


class PineconeClient:
    def __init__(self, api_key: str) -> None:
        self.client = Pinecone(api_key=api_key)


class TaskDefinitionRetriever:
    def __init__(self, database_session: Session, pinecone_client: PineconeClient) -> None:
        self.database_session = database_session
        self.pinecone_client = pinecone_client
        self.all_task_definitions = self.get_all_task_definitions()
        self.initialize_index()

    def retrieve_all_task_defintion(self) -> None:
        pass

    def get_all_task_definitions(self) -> list[str]:
        output_task_defintions = []
        all_task_defintions = task_definition.get_multi(db=self.database_session)
        for one_task_definition in all_task_defintions:
            simple_oops = TaskDefinition.from_orm(one_task_definition)
            output_task_defintions.append(simple_oops.model_dump_json(indent=2))
            print(simple_oops.model_dump_json(indent=2))
            print(120 * "-")
        return output_task_defintions

    def initialize_index(self) -> None:
        index_name = "task-definitions-te3-small-quickstart"
        existing_indexes = [index_names for index_names in self.pinecone_client.client.list_indexes().names()]

        if self.index_doesnt_exist_yet(index_name, existing_indexes):
            self.pinecone_client.client.create_index(
                index_name, dimension=1536, metric="cosine", spec=PodSpec(environment="gcp-starter", pod_type="starter")
            )
            while self.index_not_ready_yet(index_name):
                time.sleep(1)
        index = self.pinecone_client.client.Index(index_name)
        time.sleep(1)
        print(index.describe_index_stats())

    def index_doesnt_exist_yet(self, index_name: str, existing_indexes: list[str]) -> bool:
        return index_name not in existing_indexes

    def index_not_ready_yet(self, index_name: str) -> bool:
        return not self.pinecone_client.describe_index(index_name).status["ready"]

    def initialize_vector_database_index(self) -> None:
        pass

    def create_embeddings(self) -> None:
        pass

    def index_embeddings(self) -> None:
        pass


_database_session = SessionLocal()
pinecone_client = PineconeClient(settings.PINECONE_API_KEY)
task_definition_retriever = TaskDefinitionRetriever(database_session=_database_session, pinecone_client=pinecone_client)
