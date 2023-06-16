from typing import Any, Dict

from app.crud.base import CRUDBase
from app.models.task_definition import TaskDefinition
from app.schemas.task_definition import TaskDefinitionCreate, TaskDefinitionUpdate


class CRUDFlowRequest(CRUDBase[TaskDefinition, TaskDefinitionCreate, TaskDefinitionUpdate]):
    pass

task_definition = CRUDFlowRequest(TaskDefinition)