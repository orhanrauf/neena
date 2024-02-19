from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.openai_service import open_ai_service

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
    
    open_ai_service.method_that_allows_for_talking_to_openai(request)
    
    ### SANDBOX CODE ###
    
    return "Flow request executed."