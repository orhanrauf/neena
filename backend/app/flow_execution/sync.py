import os
import importlib
import inspect
import typing
from typing import List, Dict, Type
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud
from app.schemas import TaskDefinitionCreate, TaskParameter
from app import schemas
from app.flow_execution.models.base import BaseNeenaModel
from typing import Union


def get_integration_tasks(directory: str) -> Dict[str, List[Type[BaseModel]]]:
    """
    Scans the directory for integration classes and their task methods.
    Returns a dictionary with integration names as keys and lists of task methods as values.
    """
    integrations = {}
    base_package = directory.replace('/', '.')  # Convert directory path to package notation

    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            full_module_name = f"{base_package}.{module_name}"  # Construct full module name
            module = importlib.import_module(full_module_name)
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if getattr(cls, '_is_integration', False):  # Check if class is an integration
                    tasks = []
                    for method_name, method in inspect.getmembers(cls, inspect.isfunction):
                        if getattr(method, '_is_task', False):  # Check if method is a task
                            tasks.append(method)
                    if cls.__name__ not in integrations:
                        integrations[cls.__name__] = {}
                    integrations[cls.__name__]['tasks'] = tasks
                    integrations[cls.__name__]['name'] = getattr(cls, '_name', None)
                    integrations[cls.__name__]['short_name'] = getattr(cls, '_short_name', None)
                    
    return integrations

def extract_parameters_from_model(model: Union[Type[BaseNeenaModel], List[Type[BaseNeenaModel]]]) -> List[TaskParameter]:
    """
    Extracts parameters from a given model and returns a list of TaskParameter objects.
    
    Args:
        model (Union[Type[BaseNeenaModel], List[Type[BaseNeenaModel]]]): The model from which to extract parameters.
        
    Returns:
        List[TaskParameter]: A list of TaskParameter objects representing the extracted parameters.
    """
    
    if model is None:
        return []
    
    if typing.get_origin(model) is list:
        args = typing.get_args(model)
        if len(args) != 1:
            raise ValueError("List must contain exactly one type argument")
        if not issubclass(args[0], BaseNeenaModel):
            raise ValueError("Model must be a list of BaseNeenaModel")
        model = args[0]
    
    elif not issubclass(model, BaseNeenaModel):
        raise ValueError("Model must be of type BaseNeenaModel or a list of BaseNeenaModel")
    
    parameters = []
    # Use model.__annotations__ to get type information
    for i, (field_name, field_type) in enumerate(model.__annotations__.items()):
        field_info = model.model_fields[field_name]
        
        parameters.append(
            TaskParameter(
                name=field_name,
                data_type=str(field_type),
                position=i, 
                doc_string=field_info.description or "",
                optional=field_info.default is not None or field_info.default_factory is not None
            )
        )
    return parameters

def generate_example_yaml_for_list(model: Type[List[BaseNeenaModel]]) -> str:
    """
    Generates an example YAML string for a list of BaseNeenaModel objects.
    
    Args:
        model (Type[List[BaseNeenaModel]]): The model for which to generate the example YAML.
        
    Returns:
        str: A string representing the generated example YAML.
    """
    
    if typing.get_origin(model) is not list:
        raise ValueError("Model must be a typing.List")
    if len(typing.get_args(model)) != 1:
        raise ValueError("List must contain exactly one type argument")
    item_type = typing.get_args(model)[0]
    if not issubclass(item_type, BaseNeenaModel):
        raise ValueError("Model must be a list of BaseNeenaModel")
    
    # Generate example YAML for a single item
    example_item_yaml = item_type.generate_example_yaml()

    # Generate YAML for a list of 3 example items
    example_list_yaml = "\n- ".join([example_item_yaml for _ in range(3)])

    return example_list_yaml

def sync_integrations_and_tasks(directory: str, db: Session):
    """
    Syncs integration tasks with the database.

    Args:
        directory (str): The directory containing the integration tasks.
        db (Session): The database session.

    Returns:
        None
    """
    
    integrations = get_integration_tasks(directory)
    
    task_definitions = []
    
    for integration_name, fields in integrations.items():

        tasks = integrations[integration_name]['tasks']
        name = integrations[integration_name]['name']
        short_name = integrations[integration_name]['short_name']
        
        integration_create = schemas.IntegrationCreate(
            class_name=integration_name,
            name=name,
            short_name=short_name
        )
        
        # Fetch or create the integration GUID based on the integration name
        integration_guid = crud.integration.get_or_create_integration(db, integration_create)
        
        for task in tasks:
            if hasattr(task, '_task_name'):
                task_name = getattr(task, '_task_name')
                input_type = getattr(task, '_input_type', None)
                description = getattr(task, '_description', None)
                
                output_model = inspect.getfullargspec(task).annotations.get('return', None)
                
                parameters = extract_parameters_from_model(input_type)

                input_yml = input_type.generate_example_yaml() if input_type else ''
                
                if typing.get_origin(output_model) is list:
                    output_yml = generate_example_yaml_for_list(output_model)
                    output_type = f"List[{output_model.__args__[0].__name__}]"
                else:
                    if output_model == typing.Any:
                        output_yml = "Any"
                        output_type = "Any"
                    else:
                        output_yml = output_model.generate_example_yaml() if output_model else ''
                        output_type = str(output_model.__name__)

                task_definition = TaskDefinitionCreate(
                    task_name=task_name,
                    integration=integration_guid,
                    description= description,
                    parameters=parameters,
                    python_method_name=f"{task.__module__}.{task.__name__}",
                    input_type= str(input_type.__name__) if input_type else '',
                    input_yml=input_yml,
                    output_type=output_type,
                    output_yml=output_yml,
                )
                
                task_definitions.append(task_definition) 
        
    crud.task_definition.sync(task_definitions, db)
