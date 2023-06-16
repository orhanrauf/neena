from .crud_token import token
from .crud_user import user
from .crud_flow_request import flow_request
from .crud_task_definition import task_definition

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
