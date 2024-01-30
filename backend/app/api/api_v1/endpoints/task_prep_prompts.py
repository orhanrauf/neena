from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.TaskPrepPrompt)
def create_task_prep_prompt(
    *,
    db: Session = Depends(deps.get_db),
    task_prep_prompt_in: schemas.TaskPrepPromptCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create a task preparation prompt. [Details to be added]
    """
    # Implementation details to be added
    pass


@router.get("/all", response_model=List[schemas.TaskPrepPrompt])
def read_all_task_prep_prompts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all task preparation prompts.
    """
    
    response = crud.task_prep_prompt.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.TaskPrepPrompt)
def read_task_prep_prompt(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get a task preparation prompt by id. [Details to be added]
    """
    # Implementation details to be added
    pass


@router.delete("/", response_model=schemas.TaskPrepPrompt)
def remove_task_prep_prompt(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete a task preparation prompt by id. [Details to be added]
    """
    # Implementation details to be added
    pass
