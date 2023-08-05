from app.db.session import SessionLocal
from dataclasses import dataclass
from datetime import datetime
import json
import os
import sys
from types import ModuleType
from typing import List
import importlib
from uuid import UUID
from app import schemas, crud
from app.core.utils.graph import Graph, flow_to_graph
from typing import Dict
from enum import Enum
from app.execution.decorators import TaskResult
from app.schemas.task_definition import TaskDefinitionBase


class ExecutionContext:
    def __init__(self, flow: schemas.FlowBase, task_definitions: List[TaskDefinitionBase], task_modules: dict):
        self.flow = flow
        self.task_definitions = task_definitions
        self.task_modules = task_modules
        self.environment = {}  # shared variable store
        self.logs = {}  # a map from operation name to its logs
        self.task_status = {} 
        self.task_def_map = {task.id: task for task in self.task_definitions}
        self.operation_map = {operation.name: operation for operation in self.flow.task_operations}
    
    def process_logs(self, task_result: TaskResult, task_operation_id: UUID):
        task_logs = {}
        for timestamp, message in task_result.logs.items():
            # Convert Unix timestamp (milliseconds) back to datetime object
            log_time = datetime.datetime.fromtimestamp(timestamp / 1000.0)
            task_logs[task_operation_id] = TaskLog(timestamp=log_time, message=message, task_operation=task_operation_id)
        return task_logs

    def execute_flow(self):
        sorted_operation_names = FlowHandler.get_sorted_operations(self.flow)
        task_def_map = self._create_task_def_map()
        operation_map = self._create_operation_map()

        for operation_name in sorted_operation_names:
            self._execute_task(operation_name, operation_map, task_def_map)

        return self.environment

    def _create_task_def_map(self):
        return {task.id: task for task in self.task_definitions}

    def _create_operation_map(self):
        return {operation.name: operation for operation in self.flow.task_operations}

    def _execute_task(self, operation_name, operation_map, task_def_map):
        operation = operation_map[operation_name]
        task_def = task_def_map[operation.task_definition]
        task_func = getattr(self.task_modules[task_def.task_name], task_def.task_name)
        args = self._prepare_arguments(task_def, operation)
        self.task_status[operation_name] = TaskStatus.IN_PROGRESS
        output = task_func(*args, wrap_func=True)
        self.environment[operation_name] = output.result

    def _prepare_arguments(self, task_def, operation):
        args = []
        for param in sorted(task_def.parameters, key=lambda x: x.position):
            arg = self._get_matching_argument(param, operation.arguments)
            if arg.source == "@tasks()":
                source_task_name  = arg.value.split('.')[0] 
                args.append(self.environment[source_task_name])
            else:
                args.append(parse_str_to_type(arg.value, param.data_type))
        return args

    def _get_matching_argument(self, param, arguments):
        for arg in arguments:
            if arg.name == param.name:
                return arg
        return None
    
class FlowHandler:
    @staticmethod
    def flow_to_graph(flow: schemas.FlowBase) -> Graph:
        num_vertices = len(flow.task_operations)
        graph = Graph(num_vertices)
        task_to_node = {task.name: i for i, task in enumerate(flow.task_operations)}
        node_to_task = {i: task for task, i in task_to_node.items()}

        for task in flow.task_operations:
            for arg in task.arguments:
                if arg.source == "@tasks()":
                    source_task_name = arg.value.split('.')[0]
                    graph.add_edge(task_to_node[source_task_name], task_to_node[task.name])

        return graph, node_to_task

    @staticmethod
    def get_sorted_operations(flow: schemas.FlowBase) -> List[str]:
        graph, node_to_task = FlowHandler.flow_to_graph(flow)
        sorted_operation_indices = graph.topological_sort()
        sorted_operation_names = [node_to_task[i] for i in sorted_operation_indices]
        return sorted_operation_names


def parse_str_to_type(value_str: str, data_type: str):
    if data_type == 'int':
        return int(value_str)
    elif data_type == 'float':
        return float(value_str)
    elif data_type == 'bool':
        return value_str.lower() == 'true'
    elif data_type == 'str':
        return value_str
    elif data_type == 'json':
        return json.loads(value_str)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


@dataclass
class TaskLog:
    timestamp: datetime
    message: str
    task_operation: UUID
    

class TaskStatus(Enum):
    NOT_STARTED = 'not started'
    IN_PROGRESS = 'in progress'
    COMPLETED_SUCCESSFULLY = 'completed successfully'
    COMPLETED_WITH_ERRORS = 'completed with errors'
    
# Add FlowRun Class (start_time, end_time, status)
# Add TaskOperationRun Class (start_time, end_time, task_status, logs, )


class ExecutionContextFactory:
    def __init__(self):
        self.directory = os.getenv("TASK_DIRECTORY", "app/task_definitions/")
        self.db = SessionLocal()

    def create(self, flow: schemas.FlowBase) -> ExecutionContext:
        # Fetch task_definitions from the database
        task_definitions = crud.task_definition.get_multi(self.db)
        
        # Get the task module map from the directory
        task_modules = self.get_task_module_map_from_directory(self.directory)

        # Create and return an execution context
        return ExecutionContext(flow, task_definitions, task_modules)

    def get_task_module_map_from_directory(self, directory: str) -> dict:
        sys.path.insert(0, directory)
        task_modules = {}
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                module = importlib.import_module(module_name)
                for name, func in vars(module).items():
                    if callable(func) and getattr(func, '_is_neena_task', False):
                        task_modules[name] = module  # Store the module for this task
        sys.path.remove(directory)  # Clean up
        return task_modules