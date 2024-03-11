import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings

# Check if DTAP_ENV is set in the environment, indicating a cloud environment
# if "DTAP_ENVIRONMENT" not in os.environ:
#     from dotenv import load_dotenv
#     load_dotenv('.env')  # Load environment variables from .env file


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    JWT_ALGO: str = "HS512"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    DTAP_ENVIRONMENT: str
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_AUTH_ID: str

    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_API_IDENTIFIER: str
    AUTH0_RULE_NAMESPACE: str

    AZURE_TENANT_ID: str
    AZURE_KEYVAULT_NAME: str
    LOG_APPINSIGHTS: bool = False
    APPLICATIONINSIGHTS_CONNECTION_STRING: str

    TRELLO_API_KEY: str

    OPENAI_API_KEY: str

    PINECONE_API_KEY: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
