from typing import Any

from app.crud.base import CRUDBase
from app.models.flow_run import FlowRun
from sqlalchemy.orm import Session
from app.schemas import FlowRunCreate, TaskRunUpdate, FlowRunUpdate, FlowRunBase
from app.models import FlowRun, TaskRun


class CRUDFlowRun(CRUDBase[FlowRun, FlowRunCreate, FlowRunUpdate]):
    
    def create(self, db: Session, *, flow_run: FlowRunCreate) -> FlowRun:
        
        # Split information into flow_run and task_runs
        flow_run_data = flow_run.dict()
        task_run_data = flow_run_data.pop('task_runs', None)
        
        if task_run_data is None:
            raise TypeError("FlowRun contains no task run data.")
        
        # Create the FlowRun object
        db_flow_run = FlowRun(**flow_run_data)
        
        db.add(db_flow_run)
        db.commit()
        db.refresh(db_flow_run)
        
        # Get flow_run_id for the task runs
        flow_run_id = db_flow_run.id
        
        # Loop through each task run and add it to the database
        for tr in task_run_data:
            tr['flow_run_id'] = flow_run_id
            db_task_run = TaskRun(**tr)


            db.add(db_task_run)
            db.commit()
            db.refresh(db_task_run)
        
        return db_flow_run


flow_run = CRUDFlowRun(FlowRun)