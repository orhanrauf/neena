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

task_definition = CRUDTaskDefinition(TaskDefinition)