from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.IntegrationCredential)
def create_integration_credential(
    *,
    db: Session = Depends(deps.get_db),
    integration_credential_in: schemas.IntegrationCredentialCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create an integration credential.
    """

    integration_credential = crud.integration_credential.create(db, obj_in=integration_credential_in, current_user=current_user)
    return integration_credential


@router.get("/all", response_model=List[schemas.IntegrationCredential])
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
    
    response = crud.integration_credential.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.IntegrationCredential)
def read_integration_credential(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get integration credential by id.
    """
    
    return crud.integration_credential.get(db, id)


@router.delete("/", response_model=schemas.IntegrationCredential)
def remove_integration_credential(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete integration credential by id.
    """
    
    return crud.integration_credential.remove(db=db, id=id)
