from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, validator

from .task_operation import TaskOperationBase, TaskOperationInDBBase, TaskOperationUpdate
from .dependency import DependencyBase, DependencyInDBBase, DependencyUpdate


# Shared properties
class FlowBase(BaseModel):
    name: Optional[str]
    task_operations: list[TaskOperationBase]
    dependencies: list[DependencyBase]

    def topological_sort(self) -> list[TaskOperationBase]:
        graph = {task.index: [] for task in self.task_operations}
        in_degree = {task.index: 0 for task in self.task_operations}

        # Building the graph using indices
        for dependency in self.dependencies:
            graph[dependency.source_task_operation].append(dependency.target_task_operation)
            in_degree[dependency.target_task_operation] += 1

        queue = [idx for idx in graph if in_degree[idx] == 0]
        sorted_indices = []

        while queue:
            idx = queue.pop(0)
            sorted_indices.append(idx)

            for adj in graph[idx]:
                in_degree[adj] -= 1
                if in_degree[adj] == 0:
                    queue.append(adj)

        if len(sorted_indices) != len(self.task_operations):
            raise Exception("Cycle detected in the task operations")

        # Update sorted_index for each TaskOperation based on the sorted order
        sorted_tasks = []
        index_to_task = {task.index: task for task in self.task_operations}
        for sorted_idx, idx in enumerate(sorted_indices):
            task = index_to_task[idx]
            task.sorted_index = sorted_idx
            sorted_tasks.append(task)

        return sorted_tasks

    def get_sorted_task_operations(self):

        if not self.sorted:
            self.task_operations = self.topological_sort()

        return sorted(self.task_operations, key=lambda x: x.sorted_index)

    @validator("task_operations")
    def validate_task_operations_length(cls, task_operations):
        if len(task_operations) < 1:
            raise ValueError("Flow must contain at least one task operation")
        return task_operations

    @validator("dependencies")
    def validate_dependencies(cls, dependencies, values):
        task_operations = values.get("task_operations", [])
        task_operation_indexes = {task.index for task in task_operations}

        for dependency in dependencies:
            if (
                dependency.source_task_operation not in task_operation_indexes
                or dependency.target_task_operation not in task_operation_indexes
            ):
                raise ValueError("Dependency indices must point to existing task operations")

        return dependencies


# Properties to receive via API on creation
class FlowCreate(FlowBase):
    created_by_human: bool = True
    modified_by_human: bool = True


# Properties to receive via API on update
class FlowUpdate(FlowCreate):
    id: UUID
    task_operations: list[TaskOperationUpdate]
    dependencies: list[DependencyUpdate]
    modified_by_human: bool = True


class FlowInDBBase(FlowBase):
    id: UUID
    task_operations: list[TaskOperationInDBBase]
    dependencies: list[DependencyInDBBase]
    created_date: datetime
    modified_date: datetime
    created_by_email: EmailStr
    modified_by_email: EmailStr
    organization: Optional[UUID] = None
    created_by_human: Optional[bool] = True
    

    class Config:
        from_orm = True
        from_attributes = True


# Additional properties to return via API
class Flow(FlowInDBBase):
    pass


# Additional properties stored in DB
class FlowInDB(FlowInDBBase):
    pass
