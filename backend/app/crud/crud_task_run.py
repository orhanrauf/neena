from app.models.task_run import TaskRun
from app.schemas import TaskRunCreate, TaskRunUpdate
from app.crud.base import CRUDBase

class CRUDTaskPrepPrompt(CRUDBase[TaskRun, TaskRunCreate, TaskRunUpdate]):
    pass

task_run = CRUDTaskPrepPrompt(TaskRun)
