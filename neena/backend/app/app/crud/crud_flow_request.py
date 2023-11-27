from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.flow_request import FlowRequest
from app.schemas.flow_request import FlowRequestCreate, FlowRequestUpdate


class CRUDFlowRequest(CRUDBase[FlowRequest, FlowRequestCreate, FlowRequestUpdate]):
    pass

flow_request = CRUDFlowRequest(FlowRequest)