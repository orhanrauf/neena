from typing import Any, Union

from app.crud.base import CRUDBase
from app.models.flow_run import FlowRun
from sqlalchemy.orm import Session
from app.schemas import FlowRunCreate, TaskRunUpdate, FlowRunUpdate, FlowRunBase
from app.models import FlowRun, TaskRun

from typing import List
from app.schemas.task_run import TaskRunCreate
from app.models.user import User


class CRUDFlowRun(CRUDBase[FlowRun, FlowRunCreate, FlowRunUpdate]):
    def update_with_run_details(
        self, db: Session, *, db_obj: FlowRun, obj_in: Union[FlowRunUpdate, dict[str, Any]], current_user: User
    ) -> FlowRun:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "task_runs" in update_data:
            task_runs_data = update_data.pop("task_runs")
            for task_run_data in task_runs_data:
                task_run_obj = db.query(TaskRun).filter(TaskRun.id == task_run_data["id"]).first()
                if task_run_obj:
                    for key, value in task_run_data.items():
                        setattr(task_run_obj, key, value)

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        if current_user:
            db_obj.modified_by_email = current_user.email

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


flow_run = CRUDFlowRun(FlowRun)
