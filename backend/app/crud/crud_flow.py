import datetime
from typing import Any

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

    def update(self, db: Session, *, updated_flow: FlowUpdate, current_user: User):
        # Retrieve the existing Flow object from the database
        existing_flow = db.query(Flow).get(updated_flow.id)
        existing_flow.name = updated_flow.name
        existing_flow.modified_by_human = True
        existing_flow.modified_by_email = current_user.email
        existing_flow.modified_date = datetime.now()

        # Delete task operations that exist in the database but not in the updated Flow object
        for task_op in existing_flow.task_operations:
            if task_op not in flow.task_operations:
                db.delete(task_op)

        # Update task operations that exist in both the database and the updated Flow object
        for task_op in updated_flow.task_operations:
            task_op.flow = existing_flow.id
            if any(task_op.index == updated_task.index for updated_task in existing_flow.task_operations):

                # Retrieve the corresponding updated task operation
                updated_task_op = next(
                    updated_task
                    for updated_task in existing_flow.task_operations
                    if updated_task.index == task_op.index
                )

                # Perform any necessary updates to the task operation
                for attr, value in task_op.__dict__.items():
                    if attr != "index":
                        setattr(updated_task_op, attr, value)

        # Add new task operations that exist in the updated Flow object but not in the database
        for task_op in updated_flow.task_operations:
            if not any(task_op.index == existing_task_op.index for existing_task_op in existing_flow.task_operations):
                db.add(task_op)

        for dependency in updated_flow.dependencies:
            dependency.flow = existing_flow.id

            existing_dependency = next(
                (
                    dep
                    for dep in existing_flow.dependencies
                    if dep.source_task_operation == dependency.source_task_operation
                    and dep.target_task_operation == dependency.source_task_operation
                ),
                None,
            )

            if existing_dependency:
                # Update existing dependency
                for key, value in dependency.items():
                    setattr(existing_dependency, key, value)
            else:
                # Create new dependency
                new_dependency = Dependency(**dependency.model_dump())
                db.add(new_dependency)

        db.commit()


flow = CRUDFlow(Flow)
