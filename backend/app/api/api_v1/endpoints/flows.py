from typing import Any, List
from uuid import UUID
from app.core.utils.flow_validation import validate_flow

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.auth import Auth0User, auth
from app.core.flow_generator import flow_generator
from app.schemas.flow import Flow, FlowBase, FlowInDBBase
from app.schemas.task_operation import TaskOperationBase
from app.schemas.dependency import DependencyBase
from app.flow_execution.core import ExecutionContext


router = APIRouter()


@router.post("/", response_model=schemas.Flow)
def create_flow(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Body(...),
    task_operations: list[schemas.TaskOperationBase] = Body(...),
    dependencies: list[schemas.DependencyBase] = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create flow.
    """

    flow_in = schemas.FlowCreate(name=name, task_operations=task_operations, dependencies=dependencies)

    #TODO: implement flow validation

    flow = crud.flow.create(db=db, flow=flow_in, current_user=current_user)
    return schemas.Flow.from_orm(flow)


@router.put("/", response_model=schemas.Flow)
def update_flow(
    *,
    db: Session = Depends(deps.get_db),
    id: str = Body(...),
    name: str = Body(...),
    task_operations: list[schemas.TaskOperationUpdate] = Body(...),
    dependencies: list[schemas.DependencyUpdate] = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Update flow.
    """
    flow_in = schemas.FlowUpdate(name=name, id=id, task_operations=task_operations, dependencies=dependencies)
    flow = crud.flow.update(db=db, flow=flow_in, current_user=current_user)
    return schemas.Flow.from_orm(flow)

@router.get("/all", response_model=List[schemas.Flow])
def read_all_flows(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all flows.
    """

    response = crud.flow.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.Flow)
def read_flow(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
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
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete flow by id.
    """

    return crud.flow.remove(db=db, id=id)


@router.get("/generate_flow_and_execute", response_model=schemas.FlowRun)
def generate_flow_and_execute(
    *,
    db: Session = Depends(deps.get_db),
    request: str,  # TODO: should ultimately be ID
    current_user: Auth0User = Depends(auth.get_user),
) -> Flow:
    """
    Generate flow from request and execute
    """

    generated_flow_in = flow_generator.generate_flow_from_request(request)
    generated_flow_in.task_operations = generated_flow_in.topological_sort()

    generated_flow_db = crud.flow.create(db=db, flow=generated_flow_in, current_user=current_user)
    user = crud.user.get_by_email(db, email=current_user.email)
    generate_flow_schema = schemas.Flow.from_orm(generated_flow_db)

    execution_context = ExecutionContext(user=user, flow=generate_flow_schema)
    flow_run = execution_context.run_flow()

    return flow_run


@router.get("/generate", response_model=schemas.Flow)
def generate(
    *,
    db: Session = Depends(deps.get_db),
    flow_request_id: str,  # should ultimately be ID
    current_user: Auth0User = Depends(auth.get_user),
) -> Flow:
    """
    Generate flow from request
    """
    
    flow_request = crud.flow_request.get(db, flow_request_id)
    generated_flow_in = flow_generator.generate_flow_from_request(flow_request.request_instructions)
    generated_flow_in.task_operations = generated_flow_in.topological_sort()
    generated_flow_db = crud.flow.create(db=db, flow=generated_flow_in, current_user=current_user)

    return schemas.Flow.from_orm(generated_flow_db)


@router.get("/execute", response_model=schemas.FlowRun)
def execute(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Flow:
    """
    Execute flow by given ID
    """
    user = crud.user.get_by_email(db, email=current_user.email)
    flow_db = crud.flow.get(db=db, id=id)
    flow_schema = schemas.Flow.from_orm(flow_db)

    execution_context = ExecutionContext(user=user, flow=flow_schema)
    flow_run = execution_context.run_flow()

    return flow_run
