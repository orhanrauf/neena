from datetime import datetime
from typing import Any, List, Optional

from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from app.models.task_definition import TaskDefinition
from app.schemas.task_definition import TaskDefinitionCreate, TaskDefinitionUpdate


class CRUDTaskDefinition(CRUDBase[TaskDefinition, TaskDefinitionCreate, TaskDefinitionUpdate]):

    # Override get method to filter out deleted items
    def get(self, db: Session, id: Any) -> Optional[TaskDefinition]:
        return db.query(self.model).filter(self.model.id == id, self.model.deleted_at == None).first()

    # Override get_multi method to filter out deleted items
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[TaskDefinition]:
        return db.query(self.model).filter(self.model.deleted_at == None).offset(skip).limit(limit).all()

    # Override remove method to perform soft delete
    def remove(self, db: Session, *, id: str) -> TaskDefinition:
        obj = db.query(self.model).get(id)
        if obj:
            obj.deleted = True
            db.add(obj)
            db.commit()
        return obj
    
    def sync(self, task_definitions: List[TaskDefinitionCreate], db: Session) -> None:
        task_definitions_dict = {td.task_name: td for td in task_definitions if td.task_name is not None}

        existing_task_definitions = db.query(TaskDefinition).filter(TaskDefinition.deleted_at.is_(None)).all()

        for td in existing_task_definitions:
            if td.task_name in task_definitions_dict:
                task_def = task_definitions_dict.pop(td.task_name)

                # Check if any field has changed and needs update
                changes = {
                    'parameters': task_def.parameters,
                    'input_type': task_def.input_type,
                    'input_yml': task_def.input_yml,
                    'output_type': task_def.output_type,
                    'output_yml': task_def.output_yml,
                    'description': task_def.description,
                    'python_method_name': task_def.python_method_name,
                }
                
                needs_update = any(getattr(td, attr) != value for attr, value in changes.items())

                if needs_update:
                    # If updates are needed, apply changes
                    for attr, value in changes.items():
                        setattr(td, attr, value)
                    td.deleted_at = None  # Ensure the task definition is marked as active
                continue  # Move to the next iteration without creating a new entry
            
            # If the task definition no longer exists, mark it as deleted
            td.deleted_at = datetime.now()

        # For new task definitions that weren't in the existing set, create new entries
        for task_def in task_definitions_dict.values():
            if task_def.task_name:  # Ensure task_name is not None
                new_td = TaskDefinition(
                    task_name=task_def.task_name,
                    integration=task_def.integration,
                    parameters=task_def.parameters,
                    input_type=task_def.input_type,
                    input_yml=task_def.input_yml,
                    output_type=task_def.output_type,
                    output_yml=task_def.output_yml,
                    description=task_def.description,
                    python_method_name=task_def.python_method_name,
                )
                db.add(new_td)

        db.commit()

task_definition = CRUDTaskDefinition(TaskDefinition)