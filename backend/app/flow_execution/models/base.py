import json
from typing import Optional, Annotated, get_args, get_origin
from datetime import datetime, date
import typing
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
            field_type = field.annotation

            # Check if the field is Optional
            if get_origin(field_type) == typing.Union and type(None) in get_args(field_type):
                # It's an Optional, unpack the inner type
                inner_type = next(t for t in get_args(field_type) if t != type(None))
            else:
                inner_type = field_type

            if field_name == "id":
                example_value = str(uuid.uuid4())
            elif inner_type in [str, StrictStr]:
                example_value = f"{field_name}_example"
            elif inner_type in [bool, StrictBool]:
                example_value = True
            elif inner_type in [int, StrictInt]:
                example_value = 123
            elif inner_type in [float, StrictFloat]:
                example_value = 123.45
            elif inner_type == date:
                example_value = datetime.now().date().isoformat()
            elif inner_type == datetime:
                example_value = datetime.now().isoformat()
            elif inner_type == list:
                example_value = ["item1", "item2"]

            if field.alias:
                field_name = field.alias
            example[field_name] = example_value

        return yaml.dump(example, sort_keys=False)

    class Config:
        populate_by_name = True

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
