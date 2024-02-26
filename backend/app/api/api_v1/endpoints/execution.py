from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.openai_service import openai_service
from app.core.flow_generator import flow_generator

from app.core.auth import Auth0User, auth

router = APIRouter()


@router.post("/", response_model=str)
def execute_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    request: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Execute flow request.
    """

    ### SANDBOX CODE ###
    # response = openai_service.get_response_to_request(request)
    response = flow_generator.enerate_flow_from_request(request)
    ### SANDBOX CODE ###

    return response
