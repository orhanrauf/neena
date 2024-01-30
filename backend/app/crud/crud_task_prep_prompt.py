from app.models.task_prep_prompt import TaskPrepPrompt
from app.schemas import TaskPrepPromptCreate, TaskPrepPromptUpdate
from app.crud.base import CRUDBase

class CRUDTaskPrepPrompt(CRUDBase[TaskPrepPrompt, TaskPrepPromptCreate, TaskPrepPromptUpdate]):
    pass

task_prep_prompt = CRUDTaskPrepPrompt(TaskPrepPrompt)
