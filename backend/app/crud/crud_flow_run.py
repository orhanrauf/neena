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
    def update(self, db: Session, *, db_obj: FlowRun, obj_in: FlowRunUpdate, current_user: User) -> FlowRun:
        # Convert FlowRunUpdate Pydantic model to a dictionary, excluding unset fields
        update_data = obj_in.dict(exclude_unset=True, exclude={"task_runs"})

        # Iterate over the update data and set attributes on the db_obj if they exist
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # Update the 'modified_by_email' field to the current user's email
        if current_user:
            db_obj.modified_by_email = current_user.email

        # Persist changes to the database
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj
    
    def get_multi_by_flow_id(self, db: Session, flow_id: str, skip: int = 0, limit: int = 100) -> List[FlowRun]:
        return db.query(self.model).filter(self.model.flow == flow_id).order_by(self.model.modified_date.desc()).offset(skip).limit(limit).all()


flow_run = CRUDFlowRun(FlowRun)
