from sqlalchemy import UUID
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def init_db(db: Session) -> None:
    
    print(settings)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        # Create user auth
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            auth0_id=settings.FIRST_SUPERUSER_AUTH_ID
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
