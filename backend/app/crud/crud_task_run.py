from datetime import datetime
from typing import Optional
from app.models.task_run import TaskRun
from app.schemas import TaskRunCreate, TaskRunUpdate
from app.crud.base import CRUDBase
from app.models.task_prep_prompt import TaskPrepPrompt
from app.models.task_prep_answer import TaskPrepAnswer

from sqlalchemy.orm import Session

from app.schemas.user import User


class CRUDTaskRun(CRUDBase[TaskRun, TaskRunCreate, TaskRunUpdate]):

    def update_with_prep(self, db: Session, *, db_obj: TaskRun, obj_in: TaskRunUpdate, current_user: User) -> TaskRun:
        obj_data = obj_in.dict(exclude_unset=True)  # Assuming obj_in is a Pydantic model.

        # Update fields in db_obj, excluding task_prep_prompt and task_prep_answer, handle result separately
        for field, value in obj_data.items():
            if field in ["task_prep_prompt", "task_prep_answer"]:
                continue
            if field == "result":
                value = self._convert_datetime_to_iso(value)
            setattr(db_obj, field, value)

        if current_user:
            db_obj.modified_by_email = current_user.email

        db_prep_prompt = TaskPrepPrompt(**obj_in.task_prep_prompt.dict())
        db_prep_prompt.task_run = db_obj.id
        db_prep_answer = TaskPrepAnswer(**obj_in.task_prep_answer.dict())
        db_prep_answer.task_run = db_obj.id

        # Optionally, directly add the objects to the session if not done through relationships.
        db.add(db_prep_prompt)
        db.commit()
        db.refresh(db_prep_prompt)
        db.refresh(db_obj)

        db_prep_answer.task_prep_prompt = db_prep_prompt.id
        db.add(db_prep_answer)
        db.commit()
        db.refresh(db_prep_answer)
        return db_obj

    def _convert_datetime_to_iso(self, obj):
        """
        Recursively convert all datetime objects in a nested structure to ISO format strings.
        This is necessary because the default JSON serializer does not properly handle datetime objects for SQLAlchemy JSON types.
        """
        if isinstance(obj, dict):
            return {k: self._convert_datetime_to_iso(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_datetime_to_iso(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj


task_run = CRUDTaskRun(TaskRun)
