import datetime
from typing import Any, Dict, Union

from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.models.flow import Flow
from app.schemas.flow import FlowCreate, FlowUpdate
from app.models import Flow, TaskOperation, User, Dependency


class CRUDFlow(CRUDBase[Flow, FlowCreate, FlowUpdate]):
    def create(self, db: Session, *, flow: FlowCreate, current_user: User) -> Flow:

        # split information in family and members
        flow_data = flow.model_dump()

        dependency_data = flow_data.pop("dependencies")
        task_operations_data = flow_data.pop("task_operations")

        db_flow = Flow(**flow_data)
        db_flow.created_by_email = current_user.email
        db_flow.modified_by_email = current_user.email
        db_flow.created_by_human = True
        db_flow.modified_by_human = True

        db.add(db_flow)
        db.commit()
        db.refresh(db_flow)

        # get flow_id
        flow_id = db_flow.id

        # loop through task operations
        for m in task_operations_data:
            m["flow"] = flow_id
            db_task_operation = TaskOperation(**m)
            db_task_operation.created_by_email = current_user.email
            db_task_operation.modified_by_email = current_user.email

            db.add(db_task_operation)
            db.commit()
            db.refresh(db_task_operation)

        for m in dependency_data:
            m["flow"] = flow_id
            db_dependency = Dependency(**m)
            db_dependency.created_by_email = current_user.email
            db_dependency.modified_by_email = current_user.email

            db.add(db_dependency)
            db.commit()
            db.refresh(db_dependency)

        return db_flow

    def update(self, db: Session, *, flow: FlowUpdate, current_user: User) -> Flow:
        db_flow = db.query(Flow).filter(Flow.id == flow.id).first()
        flow = self._update_flow(db=db, db_obj=db_flow, obj_in=flow, current_user=current_user)
        return flow

    def _update_flow(
        self,
        db: Session,
        *,
        db_obj: Flow,
        obj_in: Union[FlowUpdate, Dict[str, Any]],
        current_user: User = None
    ) -> Flow:
        if not isinstance(obj_in, dict):
            obj_in_data = obj_in.dict(exclude_unset=True)
        else:
            obj_in_data = obj_in

        # Update the simple fields of Flow
        for key, value in obj_in_data.items():
            if key not in ['task_operations', 'dependencies'] and hasattr(db_obj, key):
                setattr(db_obj, key, value)

        # Handle TaskOperations
        new_task_operations_data = [t for t in obj_in_data['task_operations'] if t.get('id') is None]
        existing_task_operations_data = [t for t in obj_in_data['task_operations'] if t.get('id') is not None]
        
        # Update existing task operations
        for task_op_data in existing_task_operations_data:
            task_op = db.query(TaskOperation).get(task_op_data.get('id'))
            if task_op:
                for key, value in task_op_data.items():
                    setattr(task_op, key, value)

        # Add new task operations
        for task_op_data in new_task_operations_data:
            new_task_op = TaskOperation(**task_op_data)
            new_task_op.created_by_email = current_user.email
            new_task_op.modified_by_email = current_user.email
            db_obj.task_operations.append(new_task_op)

        # Delete task operations that are no longer present
        updated_task_operations_ids = {task_op_data.get('id') for task_op_data in existing_task_operations_data if task_op_data.get('id') is not None}
        for task_op in db_obj.task_operations[:]:
            if task_op.id and task_op.id not in updated_task_operations_ids:
                db.delete(task_op)

        # Handle Dependencies
        new_dependencies_data = [d for d in obj_in_data['dependencies'] if d.get('id') is None]
        existing_dependencies_data = [d for d in obj_in_data['dependencies'] if d.get('id') is not None]

        # Update existing dependencies
        for dep_data in existing_dependencies_data:
            dep = db.query(Dependency).get(dep_data.get('id'))
            if dep:
                for key, value in dep_data.items():
                    setattr(dep, key, value)

        # Add new dependencies
        for dep_data in new_dependencies_data:
            new_dep = Dependency(**dep_data)
            new_dep.created_by_email = current_user.email
            new_dep.modified_by_email = current_user.email
            db_obj.dependencies.append(new_dep)

        # Delete dependencies that are no longer present
        updated_dependencies_ids = {dep_data.get('id') for dep_data in existing_dependencies_data if dep_data.get('id') is not None}
        for dep in db_obj.dependencies[:]:
            if dep.id and dep.id not in updated_dependencies_ids:
                db.delete(dep)

        # Update modified_by_email and commit changes
        if current_user:
            db_obj.modified_by_email = current_user.email
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

flow = CRUDFlow(Flow)
