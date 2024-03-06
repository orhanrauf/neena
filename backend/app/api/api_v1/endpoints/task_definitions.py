from typing import Any, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.auth import Auth0User, auth
from app.core.task_definition_retriever import task_definition_retriever

router = APIRouter()


@router.post("/", response_model=schemas.TaskDefinition)
def create_task_definition(
    *,
    db: Session = Depends(deps.get_db),
    task_name: str = Body(...),
    parameters: list[schemas.TaskParameter] = Body(...),
    output_type: str = Body(...),
    description: str = Body(...),
    python_code: str = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create task definition.
    """

    task_definition_in = schemas.TaskDefinitionCreate(
        task_name=task_name,
        parameters=parameters,
        output_type=output_type,
        description=description,
        python_code=python_code,
    )

    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=current_user)

    return task_definition


@router.get("/all", response_model=List[schemas.TaskDefinition])
def read_all_task_definitions(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all task definitions.
    """

    return crud.task_definition.get_multi(db=db, skip=skip, limit=limit)


@router.get("/", response_model=schemas.TaskDefinition)
def read_task_definition(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get task definition by id.
    """

    return crud.task_definition.get(db, id)


@router.delete("/", response_model=schemas.TaskDefinition)
def remove_task_definition(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete task definition by id.
    """

    return crud.task_definition.remove(db=db, id=id)


@router.get("/retrieve", response_model=list[str])
def retrieve_task_definitions(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve task definitions by request.
    """

    return task_definition_retriever.get_all_task_definitions()
