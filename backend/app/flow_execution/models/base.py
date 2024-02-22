import json
from typing import Optional, Annotated
from datetime import datetime, date
import uuid
from pydantic import BaseModel, Field, StrictStr, StrictBool, StrictInt, StrictFloat
import yaml

"""
This file contains the base classes for the models used for integrations.
"""
    
class BaseAPIModel(BaseModel):
    """
    Base class for API models.
    """

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.dict(by_alias=True))

    @classmethod
    def generate_example_yaml(cls) -> str:
        """
        Generates an example YAML object from the underlying Pydantic subclass.
        """
        example = {}
        for field_name, field in cls.__fields__.items():
            example_value = None
            if field_name == 'id':
                example_value = str(uuid.uuid4())
            elif issubclass(field.type_, (StrictStr, str)):
                example_value = f"{field_name}_example"
            elif issubclass(field.type_, (StrictBool, bool)):
                example_value = True
            elif issubclass(field.type_, (StrictInt, int)):
                example_value = 123
            elif issubclass(field.type_, (StrictFloat, float)):
                example_value = 123.45
            elif issubclass(field.type_, date):
                example_value = datetime.now().date().isoformat()
            elif issubclass(field.type_, datetime):
                example_value = datetime.now().isoformat()
            elif issubclass(field.type_, list):
                example_value = ['item1', 'item2']
            if field.alias:
                field_name = field.alias
            example[field_name] = example_value
        return yaml.dump(example, sort_keys=False)
    
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