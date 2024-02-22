import os
import importlib
import inspect
from typing import List, Dict, Type
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud
from app.schemas import TaskDefinitionBase, TaskParameter
from app import schemas

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

def extract_parameters_from_model(model: Type[BaseModel]) -> List[TaskParameter]:
    parameters = []
    # Use model.__annotations__ to get type information
    for i, (field_name, field_type) in enumerate(model.__annotations__.items()):
        field_info = model.model_fields[field_name]
        
        parameters.append(
            TaskParameter(
                name=field_name,
                data_type=str(field_type),
                position=i,  # Adjust position if needed
                doc_string=field_info.description or "",
                optional=field_info.default is not None or field_info.default_factory is not None  # Adjust based on your needs
            )
        )
    return parameters


def sync_integrations_and_tasks(directory: str, db: Session):
    integrations = get_integration_tasks(directory)  # Assume this function is defined elsewhere
    for integration_name in integrations.items():

        tasks = integrations[integration_name]['tasks']
        name = integrations[integration_name]['name']
        short_name = integrations[integration_name]['short_name']
        
        integration_create = schemas.IntegrationCreate(
            class_name=integration_name,
            name=name,
            short_name=short_name
        )
        
        # Fetch or create the integration GUID based on the integration name
        integration_guid = crud.integration.get_or_create_integration(integration_name, db, integration_create)

        for task in tasks:
            if hasattr(task, '_task_name'):
                task_name = getattr(task, '_task_name')
                input_type = getattr(task, '_input_type', None)
                output_type = getattr(task, '_output_type', None)
                description = getattr(task, '_description', None)
                
                input_model = inspect.getfullargspec(task).annotations.get('return', None)
                
                parameters = extract_parameters_from_model(input_model)

                input_yml = input_type.generate_example_yaml() if input_type else ''
                output_yml = output_type.generate_example_yaml() if output_type else ''

                task_definition = TaskDefinitionBase(
                    task_name=task_name,
                    integration=integration_guid,
                    description= description,
                    parameters=parameters,  # Assume parameters extraction logic is handled elsewhere
                    python_method_name=f"{task.__module__}.{task.__name__}",
                    input_type=str(input_type.__name__) if input_type else None,
                    input_yml=input_yml,
                    output_type=str(output_type.__name__) if output_type else None,
                    output_yml=output_yml,
                    # Other necessary fields
                )
                # Sync the task definition with the database
                crud.task_definition.sync(task_definition, db)