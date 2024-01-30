from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.get("/all", response_model=List[schemas.Integration])
def read_all_integration_credentials(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all integration credentials.
    """
    
    response = crud.integration.get_multi(db=db, skip=skip, limit=limit)
    return response