
from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.TaskPrepAnswer)
def create_task_prep_answer(
    *,
    db: Session = Depends(deps.get_db),
    task_prep_answer_in: schemas.TaskPrepAnswerCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create task preparation answer.
    """

    task_prep_answer = crud.task_prep_answer.create(db, obj_in=task_prep_answer_in, current_user=current_user)
    return task_prep_answer


@router.get("/all", response_model=List[schemas.TaskPrepAnswer])
def read_all_task_prep_answers(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all task preparation answers.
    """
    
    response = crud.task_prep_answer.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.TaskPrepAnswer)
def read_task_prep_answer(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get task preparation answer by id.
    """
    
    return crud.task_prep_answer.get(db, id)


@router.delete("/", response_model=schemas.TaskPrepAnswer)
def remove_task_prep_answer(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete task preparation answer by id.
    """
    
    return crud.task_prep_answer.remove(db=db, id=id)
