from typing import Any

from app.crud.base import CRUDBase
from sqlalchemy.orm import joinedload, Session


from app.models.flow import Flow
from app.schemas.flow import FlowCreate, FlowUpdate
from app.models import Flow, TaskOperation, User


class CRUDFlow(CRUDBase[Flow, FlowCreate, FlowUpdate]):
    def create(self, db: Session, *, flow: FlowCreate, current_user: User) -> Flow:
        
        # split information in family and members
        flow_data = flow.dict()
        task_operation_data = flow_data.pop('task_operations', None)
        
        if task_operation_data is None:
            raise TypeError("Flow contains no task operation data.")
        
        db_flow = Flow(**flow_data)
        db_flow.created_by_email = current_user.email
        db_flow.modified_by_email = current_user.email
        
        db.add(db_flow)
        db.commit()
        db.refresh(db_flow)
        
        # get flow_id
        flow_id = db_flow.id
        
        # loop through task operations
        for m in task_operation_data:
            m['flow'] = flow_id
            db_task_operation = TaskOperation(**m)
            db_task_operation.created_by_email = current_user.email
            db_task_operation.modified_by_email = current_user.email

            db.add(db_task_operation)
            db.commit()
            db.refresh(db_task_operation)
        
        return db_flow

    def update(self, db: Session, *, updated_flow: FlowCreate, current_user: User):
        # Retrieve the existing Flow object from the database
        existing_flow = db.query(Flow).get(updated_flow.id)
        
        existing_flow.flow_request = updated_flow.flow_request
        existing_flow.name = updated_flow.name
        existing_flow.modified_by_human = True
        
        # Delete task operations that exist in the database but not in the updated Flow object
        for task_op in existing_flow.task_operations:
            if task_op not in flow.task_operations:
                db.delete(task_op)

        # Update task operations that exist in both the database and the updated Flow object
        for task_op in updated_flow.task_operations:
            if any(task_op.id == updated_task.id for updated_task in existing_flow.task_operations):
                # Retrieve the corresponding updated task operation
                updated_task_op = next(updated_task for updated_task in existing_flow.task_operations if updated_task.id == task_op.id)
                
                # Perform any necessary updates to the task operation
                for attr, value in task_op.__dict__.items():
                    if attr != 'id':
                        setattr(updated_task_op, attr, value)

        # Add new task operations that exist in the updated Flow object but not in the database
        for task_op in updated_flow.task_operations:
            if task_op not in existing_flow.task_operations:
                db.add(task_op)

        # Commit the changes to the database
        db.commit()

flow = CRUDFlow(Flow)