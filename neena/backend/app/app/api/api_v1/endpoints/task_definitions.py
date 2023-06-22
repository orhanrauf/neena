from typing import Any, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.TaskDefinition)
def create_task_definition(
    *,
    db: Session = Depends(deps.get_db),
    task_name: str = Body(...),
    parameters: list[schemas.TaskParameter] = Body(...),
    output_type: str = Body(...),
    output_name: str = Body(...),
    description: str = Body(...),
    python_code: str = Body(...),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create task definition.
    """

    task_definition_in = schemas.TaskDefinitionCreate(task_name=task_name, 
                                                   parameters=parameters, 
                                                   output_type=output_type,
                                                   output_name=output_name,
                                                   description=description,
                                                   python_code=python_code
                                                   )
    
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=current_user)
    
    return task_definition

@router.get("/all", response_model=List[schemas.TaskDefinition])
def read_all_task_definitions(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
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
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task definition by id.
    """
    
    return crud.flow_request.get(db, id)

@router.delete("/", response_model=schemas.TaskDefinition)
def remove_task_definition(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete task definition by id.
    """
    
    return crud.task_definition.remove(db=db, id=id)
