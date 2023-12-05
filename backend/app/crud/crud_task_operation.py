from app.crud.base import CRUDBase
from app.models.task_operation import TaskOperation
from app.schemas.task_operation import TaskOperationCreate, TaskOperationUpdate


class CRUDFlow(CRUDBase[TaskOperation, TaskOperationCreate, TaskOperationUpdate]):
    pass

task_operation = CRUDFlow(TaskOperation)