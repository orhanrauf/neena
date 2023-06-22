from fastapi import APIRouter

from app.api.api_v1.endpoints import login, proxy, task_definitions, users, flow_requests, task_operations, flows

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
api_router.include_router(flow_requests.router, prefix="/flow_requests", tags=["flow_requests"])
api_router.include_router(task_definitions.router, prefix="/task_definitions", tags=["task_definitions"])
api_router.include_router(task_operations.router, prefix="/task_operations", tags=["task_operations"])
api_router.include_router(flows.router, prefix="/flows", tags=["flows"])
