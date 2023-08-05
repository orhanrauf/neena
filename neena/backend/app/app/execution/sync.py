import os
import importlib
import sys
from datetime import datetime
from inspect import getfullargspec, getsource
from typing import Tuple, Callable, get_type_hints
from app.models.task_definition import TaskDefinition
from app.schemas import TaskDefinitionCreate, TaskDefinitionBase, TaskParameter
from sqlalchemy.orm import Session
from typing import List


def get_type_hint_str(return_hint):
    return return_hint.__name__ if isinstance(return_hint, type) else str(return_hint)

def get_task_methods_from_directory(directory: str) -> List[Tuple[str, Callable]]:
    sys.path.insert(0, directory)
    task_names = set()  # This set will store task names to check for duplicates
    task_methods = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module = importlib.import_module(module_name)
            for name, func in vars(module).items():
                if callable(func) and getattr(func, '_is_neena_task', False):
                    if name in task_names:  # Check if the task name is a duplicate
                        raise ValueError(f"Duplicate task name detected: {name}")
                    task_names.add(name)
                if callable(func) and getattr(func, '_is_neena_task', False):  # This is a task
                    task_methods.append((name, func))
    sys.path.remove(directory)  # Make sure to clean up after yourself
    return task_methods


def construct_task_definitions_from_task_methods(functions: List[Tuple[str, Callable]]) -> List[TaskDefinitionBase]:
    task_definitions = []
    for name, func in functions:
        arg_spec = getfullargspec(func.__wrapped__)
        arg_type_hints = get_type_hints(func.__wrapped__)
        task_params = [
            TaskParameter(
                name=p,
                data_type=get_type_hint_str(arg_type_hints.get(p, 'No type hint')),
                position=i
            )
            for i, p in enumerate(arg_spec.args)
        ]
        
        task_def = TaskDefinitionBase(
            task_name=name,
            parameters=task_params,
            output_type=get_type_hint_str(arg_type_hints.get('return', 'No type hint')),
            description=func.__doc__,
            python_code=getsource(func)
        )
        task_definitions.append(task_def)
    
    return task_definitions


def update_task_definitions_in_database(
    task_definitions: List[TaskDefinitionCreate],
    db: Session
) -> None:
    # Create a dictionary for quick lookup
    task_definitions_dict = {
        td.task_name: td 
        for td in task_definitions
    }

    # Fetch all existing task definitions from database
    existing_task_definitions = db.query(TaskDefinition).filter(TaskDefinition.deleted_at == None).all()

    # Update or soft-delete task definitions
    for td in existing_task_definitions:
        if td.task_name in task_definitions_dict:  # Potential update to existing task definition
            task_def = task_definitions_dict.pop(td.task_name)
            
            # Check if non-PK fields are changed
            if td.parameters != task_def.parameters or td.output_type != task_def.output_type or \
                or td.description != task_def.description or \
            td.python_code != task_def.python_code:
                # Non-PK fields have changed, soft delete old task definition
                td.deleted_at = datetime.now()

                # Create new task definition
                new_td = TaskDefinition(
                    task_name=task_def.task_name,
                    parameters=task_def.parameters,
                    output_type=task_def.output_type,
                    description=task_def.description,
                    python_code=task_def.python_code
                )
                db.add(new_td)
        else:  # Soft-delete task definition that no longer exists
            td.deleted_at = datetime.now()
    
    # Insert new task definitions
    for task_name, task_def in task_definitions_dict.items():
        new_td = TaskDefinition(
            task_name=task_name,
            parameters=task_def.parameters,
            output_type=task_def.output_type,
            description=task_def.description,
            python_code=task_def.python_code
        )
        db.add(new_td)
    
    db.commit()


    
def update_task_definitions_from_directory(directory: str, db: Session) -> None:
    task_methods = get_task_methods_from_directory(directory)
    task_definitions = construct_task_definitions_from_task_methods(task_methods)
    update_task_definitions_in_database(task_definitions, db)
    