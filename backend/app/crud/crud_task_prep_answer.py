from app.models.task_prep_answer import TaskPrepAnswer
from app.schemas import TaskPrepAnswerCreate, TaskPrepAnswerUpdate
from app.crud.base import CRUDBase

class CRUDTaskPrepAnswer(CRUDBase[TaskPrepAnswer, TaskPrepAnswerCreate, TaskPrepAnswerUpdate]):
    pass

task_prep_answer = CRUDTaskPrepAnswer(TaskPrepAnswer)
