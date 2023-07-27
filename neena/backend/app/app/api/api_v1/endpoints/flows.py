from typing import Any, List
from uuid import UUID
from app.core.utils.flow_validation import validate_flow

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.Flow)
def create_flow(
    *,
    db: Session = Depends(deps.get_db),
    flow_request: UUID = Body(...),
    name: str = Body(...),
    task_operations: list[schemas.TaskOperationBase] = Body(...),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create flow.
    """

    flow_in = schemas.FlowCreate(flow_request=flow_request, 
                                name=name,
                                task_operations=task_operations)
    
    # perform the complex validations
    validation_messages = validate_flow(flow_in, db)
    if validation_messages:
        # the request data has validation errors
        errors = [str(error) for error in validation_messages]
        return JSONResponse(status_code=422, content={"user_error": True, "errors": errors})

    
    flow = crud.flow.create(db=db, flow=flow_in, current_user=current_user)
    return flow

@router.get("/all", response_model=List[schemas.Flow])
def read_all_flows(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all flows.
    """
    
    response = crud.flow.get_multi(db=db, skip=skip, limit=limit)
    print(response)
    return response


@router.get("/", response_model=schemas.Flow)
def read_flow(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get flow by id.
    """
    
    return crud.flow.get(db, id)

@router.delete("/", response_model=schemas.Flow)
def remove_flow(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete flow by id.
    """
    
    return crud.flow.remove(db=db, id=id)
