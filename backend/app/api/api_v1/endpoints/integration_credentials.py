from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth
from app.core.secrets import key_vault
from app.models import Integration, IntegrationCredential

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

    integration_credential = crud.integration_credential.create(db, 
                                                                obj_in=integration_credential_in.model_dump(exclude={"credential"}), 
                                                                current_user=current_user)
    key_vault.set_secret(integration_credential.id, integration_credential_in.credential)
    
    return integration_credential

@router.get("/all", response_model=List[schemas.IntegrationCredential])
def read_all_integration_credentials(
    *,
    db: Session = Depends(deps.get_db),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all integration credentials for user.
    """
    
    response = crud.integration_credential.get_all_for_user(db, current_user.email)
    return response


@router.get("/", response_model=schemas.IntegrationCredential)
def update_integration_credential(
    *,
    db: Session = Depends(deps.get_db),
    integration_credential_in: schemas.IntegrationCredentialUpdate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Update integration credential by integration id and user email.
    """
    
    return crud.integration_credential.update_by_integration_and_user_email(db, integration_credential_in.id, current_user.email, integration_credential_in)


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