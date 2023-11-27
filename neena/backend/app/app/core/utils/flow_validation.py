from typing import Generator, Optional
from app import crud, schemas
from app.api import deps
from app.core.utils.graph import flow_to_graph
from app.models import (ValidationMessageBase,
                        FlowValidationFailureMessage, 
                        FlowValidationWarningMessage, 
                        TaskValidationFailureMessage,
                        TaskValidationWarningMessage)
from app.schemas.flow_request import FlowRequestBase
from app.schemas.task_definition import TaskDefinitionBase
from sqlalchemy.orm import Session
import re


def validate_flow(flow: schemas.FlowBase, db: Session) -> list[ValidationMessageBase]:
    validation_messages = []
    task_op_names = set()
    
    
    
    flow_request = crud.flow_request.get(db, flow.flow_request)
    
    if not isinstance(flow, schemas.FlowBase):
        raise TypeError("flow must be an instance of FlowBase")
    
    if not flow.name:
        validation_messages.append(FlowValidationFailureMessage("Attribute 'name' cannot be empty."))
    
    if not flow.task_operations:
        validation_messages.append(FlowValidationFailureMessage("Attribute 'task_operations' cannot be empty."))
    
    for task_op in flow.task_operations:
        if task_op.name in task_op_names:
            validation_messages.append(FlowValidationFailureMessage(f"Task operation name '{task_op.name}' is used more than once. Each Task operation in a Flow must have a unique name."))
        else:
            task_op_names.add(task_op.name)
            
        # Fetch task definition from database
        task_definition = crud.task_definition.get(db, task_op.task_definition)
        if task_definition is None:
            validation_messages.append(TaskValidationFailureMessage(f"Task definition for task {task_op.name} does not exist in the database.", task_name=task_op.name))
        else:
            validation_messages.extend(validate_task(task_op, task_definition, flow_request))
            validation_messages.extend(check_edge_validity(task_op, flow, db))
    
    if validation_messages:
        return validation_messages
    
    graph = flow_to_graph(flow)
    if graph.is_cyclic():
        validation_messages.append(FlowValidationFailureMessage("The flow has a cycle."))

    return validation_messages

    
def validate_task(task_op: schemas.TaskOperationBase,
                  task_definition: TaskDefinitionBase,
                  flow_request: FlowRequestBase) -> list[ValidationMessageBase]:
    validation_messages = [] 
    
    if not isinstance(task_op, schemas.TaskOperationBase):
        raise TypeError("task_op must be an instance of TaskOperationBase")

    # Task name should not be empty and must be alphanumeric
    if not task_op.name or not re.match('^[a-zA-Z0-9_-]*$', task_op.name):
        validation_messages.append(TaskValidationFailureMessage(f"Attribute 'name' for task cannot be empty or and can only contain letters, numbers, underscores ('_'), and hyphens ('-').", task_name=task_op.name))
    
    if task_definition is None:
        validation_messages.append(TaskValidationFailureMessage(f"Task definition for task {task_op.name} does not exist in the database.", task_name=task_op.name))
    else:
        validation_messages.extend(check_task_attributes_empty(task_op))
        validation_messages.extend(check_task_arguments(task_op, task_definition, flow_request))
        
    return validation_messages


def check_task_attributes_empty(task_op: schemas.TaskOperationBase) -> Generator[FlowValidationFailureMessage, None, None]:
    attributes = task_op.__annotations__
    for attr_name, attr_type in attributes.items():
        if attr_name.startswith("_") or attr_name=='explanation': # explanation attribute is not required
            continue
        if attr_name not in task_op.__dict__:
            yield TaskValidationFailureMessage(f"Attribute '{attr_name}' cannot be empty for {task_op.name}", task_name=task_op.name)
    return


def check_task_arguments(task_op: schemas.TaskOperationBase, 
                         task_definition: schemas.TaskDefinitionBase, 
                         flow_request: FlowRequestBase) -> list[ValidationMessageBase]:
    validation_messages = [] 

    # Check that arguments match parameters: existence, type
    params = {param.name: param.data_type for param in task_definition.parameters}

    valid_sources = ["@tasks()", "@context()", "@metadata()"]

    for arg in task_op.arguments:
        try:
            if arg.data_type != params[arg.name]:
                validation_messages.append(TaskValidationFailureMessage(f"Data type of argument {arg.name} does not match the corresponding parameter in task {task_op.name}.", task_name=task_op.name))
            if arg.source not in valid_sources:
                validation_messages.append(TaskValidationFailureMessage(f"Invalid source for argument {arg.name} in task {task_op.name}. Source should be one of @tasks(), @context(), @metadata().", task_name=task_op.name))
            if arg.source == "@metadata()":
                if not any(arg.value in d.values() for d in flow_request.request_metadata):
                    validation_messages.append(TaskValidationFailureMessage(f"Value {arg.value} for argument {arg.name} in task {task_op.name} does not exist in the flow request metadata.", task_name=task_op.name))

        except KeyError:
            validation_messages.append(TaskValidationFailureMessage(f"Argument {arg.name} for task {task_op.name} does not exist in task definition parameters.", task_name=task_op.name))

    return validation_messages


def check_edge_validity(task_op: schemas.TaskOperationBase, flow: schemas.FlowBase, db: Session) -> list[ValidationMessageBase]:
    validation_messages = [] 

    for arg in task_op.arguments:
        if arg.source == "@tasks()":
            # Check if the argument value is correctly formatted
            if '.' not in arg.value or arg.value.split('.')[-1] != "output":
                validation_messages.append(TaskValidationFailureMessage(f"Invalid value format for argument {arg.name} in task {task_op.name}. When the source is '@tasks()', value should be in the format of 'task_name.output'.", task_name=task_op.name))
                continue
                
            task_output_source = arg.value.split('.')[-2]  # The task's output that is being used as an argument source
            source_task_op = [task for task in flow.task_operations if task.name == task_output_source]
            
            if not source_task_op:
                validation_messages.append(TaskValidationFailureMessage(f"The source task operation {task_output_source} does not exist in the flow for task {task_op.name}.", task_name=task_op.name))
                continue

            source_task_op = source_task_op[0]
            source_task_definition = crud.task_definition.get(db, source_task_op.task_definition)
            
            if source_task_definition is None:
                validation_messages.append(TaskValidationFailureMessage(f"Task definition for task {source_task_op.name} does not exist in the database.", task_name=source_task_op.name))
                continue
            # The data type of argument should match the data type of output of source task operation
            if arg.data_type != source_task_definition.output_type:
                validation_messages.append(TaskValidationFailureMessage(f"The data type of argument {arg.name} does not match the output type of the source task operation {task_output_source} for task {task_op.name}.", task_name=task_op.name))

    return validation_messages