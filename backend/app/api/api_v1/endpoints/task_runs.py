from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.TaskRun)
def create_task_run(
    *,
    db: Session = Depends(deps.get_db),
    task_run_in: schemas.TaskRunCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create task run.
    """

    task_run = crud.task_run.create(db, obj_in=task_run_in, current_user=current_user)
    return task_run


@router.get("/all", response_model=List[schemas.TaskRun])
def read_all_task_runs(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all task runs.
    """
    
    response = crud.task_run.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.TaskRun)
def read_task_run(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get task run by id.
    """
    
    return crud.task_run.get(db, id)

@router.delete("/", response_model=schemas.TaskRun)
def remove_task_run(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete task run by id.
    """
    
    return crud.task_run.remove(db=db, id=id)