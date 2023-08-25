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
    
    def sync(task_definitions: List[TaskDefinitionCreate], db: Session) -> None:
        
        # Create a dictionary for quick lookup
        task_definitions_dict = {
            td.task_name: td 
            for td in task_definitions
        }

        # Fetch all existing task definitions from database
        existing_task_definitions = db.query(TaskDefinition).filter(TaskDefinition.deleted_at == None).all()

        # Update or soft-delete task definitions
        for td in existing_task_definitions:
            if td.task_name in task_definitions_dict:  # Potential update to existing task definition
                task_def = task_definitions_dict.pop(td.task_name)
                
                # Check if non-PK fields are changed
                if td.parameters != task_def.parameters or td.output_type != task_def.output_type \
                    or td.description != task_def.description or \
                td.python_code != task_def.python_code:
                    # Non-PK fields have changed, soft delete old task definition
                    td.deleted_at = datetime.now()

                    # Create new task definition
                    new_td = TaskDefinition(
                        task_name=task_def.task_name,
                        parameters=task_def.parameters,
                        output_type=task_def.output_type,
                        description=task_def.description,
                        python_code=task_def.python_code
                    )
                    db.add(new_td)
            else:  # Soft-delete task definition that no longer exists
                td.deleted_at = datetime.now()
        
        # Insert new task definitions
        for task_name, task_def in task_definitions_dict.items():
            new_td = TaskDefinition(
                task_name=task_name,
                parameters=task_def.parameters,
                output_type=task_def.output_type,
                description=task_def.description,
                python_code=task_def.python_code
            )
            db.add(new_td)
        
        db.commit()

task_definition = CRUDTaskDefinition(TaskDefinition)