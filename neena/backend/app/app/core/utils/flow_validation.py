from typing import Generator, Optional
from app import crud, schemas
from app.api import deps
from app.core.utils.graph import flow_to_graph
from app.models import (ValidationMessageBase,
                        FlowValidationFailureMessage, 
                        FlowValidationWarningMessage, 
                        TaskValidationFailureMessage,
                        TaskValidationWarningMessage)
from sqlalchemy.orm import Session
import re


def validate_flow(flow: schemas.FlowBase, db: Session) -> list[ValidationMessageBase]:
    validation_messages = []
    
    if not flow.name:
        validation_messages.append(FlowValidationFailureMessage("Attribute 'name' cannot be empty."))
    
    if not flow.task_operations:
        validation_messages.append(FlowValidationFailureMessage("Attribute 'task_operations' cannot be empty."))
    
    for task_op in flow.task_operations:
        validation_messages.extend(validate_task(task_op, flow, db))
        validation_messages.extend(check_edge_validity(task_op, flow, db))
        
    graph = flow_to_graph(flow)
    if graph.is_cyclic():
        validation_messages.append(FlowValidationFailureMessage("The flow has a cycle."))

    return validation_messages

    
def validate_task(task_op: schemas.TaskOperationBase, 
                  flow: schemas.FlowBase, 
                  db: Session) -> list[ValidationMessageBase]:
    validation_messages = [] 

    # Task name should not be empty and must be alphanumeric
    if not task_op.name or not re.match('^[a-zA-Z0-9]*$', task_op.name):
        validation_messages.append(TaskValidationFailureMessage(f"Attribute 'name' for task {task_op.name} cannot be empty or non-alphanumeric."))

    # Fetch task definition from database
    task_definition = crud.task_definition.get(db, task_op.task_definition)
    
    if task_definition is None:
        validation_messages.append(TaskValidationFailureMessage(f"Task definition for task {task_op.name} does not exist in the database."))
    else:
        validation_messages.extend(check_task_attributes_empty(task_op))
        validation_messages.extend(check_task_arguments(task_op, task_definition))
        validation_messages.extend(check_task_output(task_op, task_definition))

    return validation_messages


def check_task_attributes_empty(task_op: schemas.TaskOperationBase) -> Generator[FlowValidationFailureMessage, None, None]:
    attributes = task_op.__annotations__
    for attr_name, attr_type in attributes.items():
        if attr_name.startswith("_") or issubclass(attr_type, Optional): # explanation attribute is required for example
            continue
        if attr_name not in task_op.__dict__:
            yield TaskValidationFailureMessage(f"Attribute '{attr_name}' cannot be empty for {task_op.name}")
    return


def check_task_arguments(task_op: schemas.TaskOperationBase, task_definition: schemas.TaskDefinitionBase) -> list[ValidationMessageBase]:
    validation_messages = [] 

    # Check that arguments match parameters: existence, type
    params = {param.name: param.data_type for param in task_definition.parameters}
    args = {arg.name: arg.data_type for arg in task_op.arguments}

    for arg in args:
        if arg not in params:
            validation_messages.append(TaskValidationFailureMessage(f"Argument {arg} does not exist in parameters for task {task_op.name}."))
        if args[arg] != params[arg]:
            validation_messages.append(TaskValidationFailureMessage(f"Data type of argument {arg} does not match the corresponding parameter in task {task_op.name}."))

    return validation_messages

def check_task_output(task_op: schemas.TaskOperationBase, task_definition: schemas.TaskDefinitionBase) -> list[ValidationMessageBase]:
    validation_messages = [] 

    # Check that output matches task definition's parameters: existence, nullability and type
    if task_op.output_type != task_definition.output_type:
        validation_messages.append(TaskValidationFailureMessage(f"Output type of task {task_op.name} does not match with the task definition."))
    if task_op.output_name != task_definition.output_name:
        validation_messages.append(TaskValidationFailureMessage(f"Output name of task {task_op.name} does not match with the task definition."))
    

    return validation_messages

def check_edge_validity(task_op: schemas.TaskOperationBase, flow: schemas.FlowBase, db: Session) -> list[ValidationMessageBase]:
    validation_messages = [] 

    for arg in task_op.arguments:
        if arg.source == "@tasks()":
            task_output_source = arg.value.split('.')[-2]  # The task's output that is being used as an argument source
            source_task_op = [task for task in flow.task_operations if task.name == task_output_source]
            
            if not source_task_op:
                validation_messages.append(TaskValidationFailureMessage(f"The source task operation {task_output_source} does not exist in the flow for task {task_op.name}."))
                continue

            source_task_op = source_task_op[0]
            source_task_definition = crud.task_definition.get(db, source_task_op.task_definition)

            # The data type of argument should match the data type of output of source task operation
            if arg.data_type != source_task_definition.output_type:
                validation_messages.append(TaskValidationFailureMessage(f"The data type of argument {arg.name} does not match the output type of the source task operation {task_output_source} for task {task_op.name}."))

            # If the argument is not nullable, the output of the source task operation should also be not nullable
            if arg.nullable == False and source_task_definition.output_name is None:
                validation_messages.append(TaskValidationFailureMessage(f"The source task operation {task_output_source} output is nullable, but the argument {arg.name} in task {task_op.name} is not."))

    return validation_messages