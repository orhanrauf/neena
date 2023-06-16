from typing import Any, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.FlowRequest)
def create_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    request_metadata: dict = Body(...),
    request_instructions: str = Body(...),
    request_body: str = Body(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create flow request.
    """

    flow_request_in = schemas.FlowRequestCreate(request_metadata=request_metadata, 
                                                request_instructions=request_instructions, 
                                                request_body=request_body)
    
    flow_request = crud.flow_request.create(db, obj_in=flow_request_in, current_user=current_user)
    
    return flow_request

@router.get("/all", response_model=List[schemas.FlowRequest])
def read_all_flow_requests(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all flow requests.
    """
    
    response = crud.flow_request.get_multi(db=db, skip=skip, limit=limit)
    print(response)
    return response


@router.get("/", response_model=schemas.FlowRequest)
def read_flow_request(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
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
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete flow request by id.
    """
    
    return crud.flow_request.remove(db=db, id=id)
