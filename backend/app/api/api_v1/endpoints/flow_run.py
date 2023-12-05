from ast import List
from typing import Any, Dict, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings


router = APIRouter()

@router.get("/all", response_model=List[schemas.FlowRun])
def read_all_flows_runs(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all flow runs.
    """
    response = crud.flow.get_multi(db=db, skip=skip, limit=limit)
    print(response)
    return response

@router.get("/", response_model=List[schemas.FlowRun])
def read_all_for_flow_id(
    *,
    db: Session = Depends(deps.get_db),
    flow_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all flow_runs by flow_id.
    """
    
    return crud.flow_run.get_multi_for_flow_id(db, id, skip: int = 0, limit: int = 100)