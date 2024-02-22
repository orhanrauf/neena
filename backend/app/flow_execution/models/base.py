import json
from typing import Optional, Annotated
from datetime import datetime, date
import uuid
from pydantic import BaseModel, Field, StrictStr, StrictBool, StrictInt, StrictFloat
import yaml

"""
This file contains the base classes for the models used for integrations.
"""

class BaseNeenaModel(BaseModel):
    """
    Contains common functionality for Neena models.
    """
    
    @classmethod
    def generate_example_yaml(cls) -> str:
            """
            Generates an example YAML object from the underlying Pydantic subclass.

            Returns:
                str: The generated example YAML object.
            """
            example = {}
            for field_name in cls.model_fields:
                field = cls.model_fields[field_name]
                example_value = None
                if field_name == 'id':
                    example_value = str(uuid.uuid4())
                elif field.annotation is str or field.annotation is StrictStr:
                    example_value = f"{field_name}_example"
                elif field.annotation is bool or field.annotation is StrictBool:
                    example_value = True
                elif field.annotation is int or field.annotation is StrictInt:  # Adjusted to direct comparison
                    example_value = 123
                elif field.annotation is float or field.annotation is StrictFloat:  # Adjusted to direct comparison
                    example_value = 123.45
                elif field.annotation is date:  # Adjusted to direct comparison
                    example_value = datetime.now().date().isoformat()
                elif field.annotation is datetime:  # Adjusted to direct comparison
                    example_value = datetime.now().isoformat()
                elif field.annotation is list:  # Adjusted to direct comparison
                    example_value = ['item1', 'item2']

                if field.alias:
                    field_name = field.alias
                example[field_name] = example_value
                
            return yaml.dump(example, sort_keys=False)
            
    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.model_dump(by_alias=True))
    
class BaseAPIModel(BaseNeenaModel):
    """
    Base class for API models.
    """

    
class BaseIntegrationActionModel(BaseNeenaModel):
    """
    Base class for integration action models.
    
    These models are used to represent the data that is sent to a Neena task and usually take the form of 
    CRUD operations.
    
    Example: CardCreate, CardUpdate, CardDelete for Trello integration.
    """