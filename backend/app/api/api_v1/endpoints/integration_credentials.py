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
def create_or_update_by_integration_and_user_email(
    *,
    db: Session = Depends(deps.get_db),
    integration_credential_in: schemas.IntegrationCredentialCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create an integration credential.
    """

    integration_credential_db = crud.integration_credential.get_by_integration_and_user_email(
        db, integration_credential_in.integration, current_user.email
    )
    
    if integration_credential_db:
        integration_credential_db = crud.integration_credential.update_by_integration_and_user_email(
            db, current_user.email, integration_credential_in
        )
        key_vault.set_secret(integration_credential_db.id, integration_credential_in.credential)
        integration_credential = integration_credential_db
        
    else:
        integration_credential = crud.integration_credential.create(db, obj_in=integration_credential_in, current_user=current_user)
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
    
    key_vault.delete_secret(id)

    return crud.integration_credential.remove(db=db, id=id)
