from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.auth import Auth0User, auth


router = APIRouter()

@router.get("/all", response_model=List[schemas.FlowRun])
def read_all_flows_runs(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all flow runs.
    """
    response = crud.flow_run.get_multi(db=db, skip=skip, limit=limit)
    return response

@router.post("/", response_model=schemas.FlowRun)
def create_flow_run(
    *,
    db: Session = Depends(deps.get_db),
    flow_run_in: schemas.FlowRunCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create flow run.
    """

    flow_run = crud.flow_run.create(db, obj_in=flow_run_in, current_user=current_user)
    return flow_run

@router.get("/", response_model=schemas.FlowRun)
def read_flow_run(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get flow run by id.
    """
    
    return crud.flow_run.get(db, id)

@router.get("/all_for_flow_id", response_model=List[schemas.FlowRun])
def read_all_for_flow_id(
    *,
    db: Session = Depends(deps.get_db),
    flow_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get all flow runs by flow_id.
    """
    
    return crud.flow_run.get_multi_by_flow_id(db, flow_id, skip=skip, limit=limit)