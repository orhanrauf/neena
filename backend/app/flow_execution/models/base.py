import json
from pydantic import BaseModel

"""
This file contains the base classes for the models used for integrations.
"""
    


class BaseAPIModel(BaseModel):
    """
    Base class for API models.
    """
    
    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())
    

class BaseIntegrationActionModel(BaseModel):
    """
    Base class for integration action models.
    
    These models are used to represent the data that is sent to a Neena task and usually take the form of 
    CRUD operations.
    
    Example: CardCreate, CardUpdate, CardDelete for Trello integration.
    """
    
    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())