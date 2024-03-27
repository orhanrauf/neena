from datetime import datetime, timezone
import importlib
import inspect
from pprint import pprint
from fastapi import Depends
from pydantic import BaseModel
from typing import Any, Dict, List, Type
from uuid import UUID

from app import crud, schemas
from app.db.session import SessionLocal
from app.flow_execution.integrations.base import BaseIntegration
from app.schemas.task_definition import TaskDefinition
from app.schemas.flow import Flow, FlowBase
from app.schemas.flow_run import FlowRun, FlowRunBase
from app.flow_execution.decorators import TaskResult
from app.schemas.task_prep_answer import TaskPrepAnswerBase
from app.schemas.task_prep_prompt import TaskPrepPromptBase, TaskPrepPromptCreate
from app.core.task_preparation_generator import task_preparation_generator
from app.core.shared_models import FlowStatus, TaskStatus
from app.schemas.task_operation import TaskOperationBase
from app.schemas.task_run import TaskRun, TaskRunBase
from sqlalchemy.orm import Session

from app.api import deps

class ExecutionContext:
    """
    The ExecutionContext class is responsible for running a flow and executing its tasks,
    as well as managing the state of the flow run.
    """

    def __init__(self, db: Session, user: schemas.User, flow: Flow, flow_request: schemas.FlowRequest, flow_run: FlowRun = None):
        self.user = user
        self.flow = flow
        flow.topological_sort()
        self.integrations_cache: Dict[UUID, BaseIntegration] = {}
        self.db = SessionLocal() if not db else db
        self.path_to_integrations = "app.flow_execution.integrations"
        self.flow_run = flow_run
        self.flow_request = flow_request

    def run_flow(self) -> FlowRun:
        """
        Executes all tasks in a flow. This is the main entry point for running a flow.

        This method does the following:
        1. Instantiates the flow run if not given.
        2. Iterates over and executes all tasks in the flow, interfacing with the integrations and
           TaskPreparationGenerator and updating the task run states as needed.
        3. Updates the flow run status to "completed" when all tasks have been executed successfully, or "failed" if any task fails.
        """

        flow_run = self._instantiate_flow_run(self.flow)
        
        try:
            for task_op in self.flow.task_operations:
                task_run = self._run_task(task_op)
                if task_run.status == TaskStatus.FAILED:
                    return self._close_flow_run_failure(flow_run)

            return self._close_flow_run_success(flow_run)
        except Exception as e:
            return self._close_flow_run_failure(flow_run)

    def _close_flow_run_failure(self, flow_run: FlowRun) -> FlowRun:
        """
        Updates the status of a flow run to "failed" and sets its end time.
        """
        flow_run.status = FlowStatus.FAILED
        flow_run.end_time = datetime.now()
        flow_run_db = crud.flow_run.get(db=self.db, id=flow_run.id)
        return crud.flow_run.update(db=self.db, db_obj=flow_run_db, obj_in=flow_run, current_user=self.user)

    def _close_flow_run_success(self, flow_run: FlowRun) -> FlowRun:
        """
        Updates the status of a flow run to "completed" and sets its end time.
        """
        flow_run.status = FlowStatus.COMPLETED
        flow_run.end_time = datetime.now()
        flow_run_db = crud.flow_run.get(db=self.db, id=flow_run.id)
        return crud.flow_run.update(db=self.db, db_obj=flow_run_db, obj_in=flow_run, current_user=self.user)

    def _run_task(self, task_op: TaskOperationBase) -> TaskRun:
        """
        Runs a task operation and returns the result.
        """

        task_run = self._instantiate_task_run(task_op)

        task_definition = self._get_task_definition(task_op.task_definition)
        task_prep_prompt, task_prep_answer = self._prepare_task(task_definition, task_op.index)

        pprint(task_prep_prompt.messages[1])

        task_result = self._execute_task(task_definition, task_prep_answer)

        task_run = self._close_task_run(task_run, task_result, task_prep_prompt, task_prep_answer)

        return task_run

    def _close_task_run(
        self,
        task_run: TaskRun,
        task_result: TaskResult,
        task_prep_prompt: TaskPrepPromptBase,
        task_prep_answer: TaskPrepAnswerBase,
    ) -> TaskRun:
        """
        Closes a task run by updating its status and end time. Formats the task run from the task result.
        """

        # task_run.task_prep_prompt = TaskPrepPrompt(**task_prep_prompt.dict())
        # task_run.task_prep_answer = TaskPrepAnswer(**task_prep_answer.dict())

        task_run.task_prep_prompt = task_prep_prompt
        task_run.task_prep_answer = task_prep_answer

        if isinstance(task_result.data, list):
            task_run.result = task_result.data
        elif isinstance(task_result.data, dict):
            task_run.result = task_result.data
        elif task_result.data is None:
            task_run.result = None
        else:
            task_run.result = task_result.data.dict()

        # task_run.result = task_result.data
        task_run.status = task_result.status
        task_run.end_time = datetime.now(tz=timezone.utc)

        task_run_db = crud.task_run.get(db=self.db, id=task_run.id)

        return crud.task_run.update_with_prep(
            db=self.db, db_obj=task_run_db, obj_in=task_run, current_user=self.user
        )

    def _instantiate_task_run(self, task_op: TaskOperationBase) -> TaskRun:
        """
        Instantiates a task run for the given task operation.
        Writes to DB, updates self, and returns the task run object.

        Args:
            task_op (TaskOperationBase): The task operation for which the task run is being instantiated.

        Returns:
            TaskRun: The instantiated task run.
        """
        task_run = TaskRunBase(
            flow_run=self.flow_run.id,
            task_operation_index=task_op.index,
            status=TaskStatus.IN_PROGRESS,
            start_time=datetime.now(),
        )
        task_run_db = crud.task_run.create(db=self.db, obj_in=task_run, current_user=self.user)

        task_run = TaskRun.from_orm(task_run_db)

        self.flow_run.task_runs.append(task_run)

        self.current_task_run = task_run

        return task_run

    def _prepare_task(
        self, task_definition: TaskDefinition, task_operation_index: int
    ) -> tuple[TaskPrepPromptBase, TaskPrepAnswerBase]:
        """
        Prepares a task for execution by generating a prompt and sending it to the TaskPreparationGenerator.
        """
        task_prep_prompt, task_prep_answer = task_preparation_generator.generate(
            self.flow, self.flow_run, task_operation_index, task_definition, self.flow_request
        )
        return task_prep_prompt, task_prep_answer

    def _get_task_definition(self, task_definition_id: UUID) -> TaskDefinition:
        """
        Retrieves a task definition by its ID.
        """
        return schemas.TaskDefinition.from_orm(crud.task_definition.get(self.db, task_definition_id))

    def _instantiate_flow_run(self, flow: FlowBase) -> FlowRun:
        """
        Instantiates a flow run for the given flow if not already instantiated.
        Adds to self, writes to database, and returns the flow run object.
        """
        
        if self.flow_run:
            return self.flow_run

        flow_run = FlowRunBase(
            flow=flow.id, status=FlowStatus.IN_PROGRESS, triggered_time=datetime.now(), triggered_by=self.user.email
        )

        self.flow_run = schemas.FlowRun.from_orm(
            crud.flow_run.create(db=self.db, obj_in=flow_run, current_user=self.user)
        )

        return self.flow_run

    def _execute_task(self, task_definition: TaskDefinition, task_prep_answer: TaskPrepAnswerBase) -> TaskResult:
        """
        Executes a task based on its definition and provided parameters.

        Returns the result of the task execution, which is a TaskResponse object.
        """
        integration_instance = self._get_integration_instance(task_definition.integration)

        actual_python_name = task_definition.python_method_name.split(".")[-1]

        method = getattr(integration_instance, actual_python_name)

        input_type = self._get_method_input_type(integration_instance, actual_python_name)

        if input_type is None:
            return method()
        else:
            task_input_params = self._parse_parameters(task_prep_answer)
            task_input = input_type(**task_input_params)
            return method(task_input)

    def _parse_parameters(self, task_prep_answer: TaskPrepAnswerBase) -> Dict[str, Any]:
        """
        Parses the parameters from the task preparation answer.
        """
        return {param.name: param.value for param in task_prep_answer.parameters}

    def _get_method_input_type(self, integration_instance: BaseIntegration, method_name: str) -> Type[BaseModel] | None:
        """
        Introspectively fetches the input type of a Task of an Integration instance.
        Assumes the task method has only one parameter besides 'self' and it's a Pydantic model
        """
        method = getattr(integration_instance, method_name)
        sig = inspect.signature(method)

        parameter = next(iter(sig.parameters.values()), None)

        return parameter.annotation if parameter else None

    def _get_integration_instance(self, integration_id: UUID) -> BaseIntegration:
        """
        Retrieves or creates an integration instance by its ID.
        """
        if integration_id in self.integrations_cache:
            return self.integrations_cache[integration_id]

        integration = schemas.Integration.from_orm(crud.integration.get(self.db, integration_id))

        path_to_integration = f"{self.path_to_integrations}.{integration.short_name}"

        module = importlib.import_module(path_to_integration)
        integration_class = getattr(module, integration.class_name)

        integration_instance = integration_class(self.user)
        self.integrations_cache[integration_id] = integration_instance
        return integration_instance
