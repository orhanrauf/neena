import os
import importlib
import inspect
from typing import List, Dict, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud
from app.schemas import TaskDefinitionBase, TaskParameter

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
                    integrations[cls.__name__] = tasks
    return integrations

def extract_parameters_from_model(model: Type[BaseModel]) -> List[TaskParameter]:
    """
    Extracts parameters from a Pydantic model.
    """
    parameters = []
    for field_name, field in model.__fields__.items():
        parameters.append(
            TaskParameter(
                name=field_name,
                data_type=field.type_.__name__,
                position=field.field_info.extra.get('position', 0),
                doc_string=field.field_info.description or "",
                optional=field.allow_none
            )
        )
    return parameters

def sync_integrations_and_tasks(directory: str, db: Session):
    """
    Synchronizes integration classes and their tasks with the database.
    """
    integrations = get_integration_tasks(directory)
    for integration_name, tasks in integrations.items():
        for task in tasks:
            # Assume the first argument after 'self' is the input model
            input_model = inspect.getfullargspec(task).annotations.get('return', None)
            task_params = extract_parameters_from_model(input_model) if input_model else []
            # Create or update the task definition in the database
            task_definition = TaskDefinitionBase(
                task_name=task.__name__,
                integration=integration_name,
                parameters=task_params,
                python_method_name=task.__module__ + "." + task.__name__,
                # Other fields as necessary
            )
            # Assuming a CRUD utility to sync task definitions
            crud.task_definition.sync(task_definition, db)


#TODO:
# Add integration and task booleans to decorator wrappers
# Add other fields to task_definition
# Add position for parameters
# Add field name for task definition
# Check __name__ usage currently with __module__ + "." + __name__ stuff
# Add step to get YML definition of output models
