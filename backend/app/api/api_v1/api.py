from fastapi import APIRouter

from app.api.api_v1.endpoints import task_definitions, users, flow_requests, task_operations, flows, flow_runs, dependencies, task_runs, task_prep_prompts, task_prep_answers, integration_credentials, integrations

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(flow_requests.router, prefix="/flow_requests", tags=["flow_requests"])
api_router.include_router(task_definitions.router, prefix="/task_definitions", tags=["task_definitions"])
api_router.include_router(task_operations.router, prefix="/task_operations", tags=["task_operations"])
api_router.include_router(flows.router, prefix="/flows", tags=["flows"])
api_router.include_router(flow_runs.router, prefix="/flow_runs", tags=["flow_runs"])
api_router.include_router(dependencies.router, prefix="/dependencies", tags=["dependencies"])
api_router.include_router(task_runs.router, prefix="/task_runs", tags=["task_runs"])
api_router.include_router(task_prep_prompts.router, prefix="/task_prep_prompts", tags=["task_prep_prompts"])
api_router.include_router(task_prep_answers.router, prefix="/task_prep_answers", tags=["task_prep_answers"])
api_router.include_router(integration_credentials.router, prefix="/integration_credentials", tags=["integration_credentials"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(integrations.router, prefix="/execution", tags=["execution"])
