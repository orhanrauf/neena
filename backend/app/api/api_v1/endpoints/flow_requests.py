from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.FlowRequest)
def create_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    flow_request_in: schemas.FlowRequestCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create flow request.
    """

    flow_request = crud.flow_request.create(db, obj_in=flow_request_in, current_user=current_user)
    return flow_request

@router.put("/", response_model=schemas.FlowRequest)
def update_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    flow_request_in: schemas.FlowRequestUpdate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Update flow request.
    """
    
    flow_request = crud.flow_request.get(db, flow_request_in.id)
    flow_request = crud.flow_request.update(db, db_obj=flow_request, obj_in=flow_request_in, current_user=current_user)
    return flow_request


@router.get("/all", response_model=List[schemas.FlowRequest])
def read_all_flow_requests(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all flow requests.
    """
    
    response = crud.flow_request.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.FlowRequest)
def read_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get flow request by id.
    """
    
    return crud.flow_request.get(db, id)

@router.delete("/", response_model=schemas.FlowRequest)
def remove_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete flow request by id.
    """
    
    return crud.flow_request.remove(db=db, id=id)
