from typing import Any, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.shared_models import Argument
from app.api import deps
from app.core.auth import Auth0User, auth

router = APIRouter()


@router.post("/", response_model=schemas.TaskOperation)
def create_task_operation(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Body(...),
    task_definition: str = Body(...),
    arguments: list[Argument] = Body(...),
    flow: str = Body(...),
    explanation: str = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create task operation.
    """

    task_operation_in = schemas.TaskOperationCreate(name=name, 
                                                   task_definition=task_definition, 
                                                   arguments=arguments,
                                                   flow=flow,
                                                   explanation=explanation
                                                   )
    
    task_operation = crud.task_operation.create(db, obj_in=task_operation_in, current_user=current_user)
    
    return task_operation

@router.get("/all", response_model=List[schemas.TaskOperation])
def read_all_task_operations(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all task operations.
    """
    
    return crud.task_operation.get_multi(db=db, skip=skip, limit=limit)


@router.get("/", response_model=schemas.TaskOperation)
def read_task_operation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get task operation by id.
    """
    
    return crud.flow_request.get(db, id)

@router.delete("/", response_model=schemas.TaskOperation)
def remove_task_operation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete task operation by id.
    """
    
    return crud.task_operation.remove(db=db, id=id)
