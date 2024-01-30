from app.models.dependency import Dependency
from app.schemas import DependencyCreate, DependencyUpdate
from app.crud.base import CRUDBase

class CRUDDependency(CRUDBase[Dependency, DependencyCreate, DependencyUpdate]):
    pass

dependency = CRUDDependency(Dependency)
