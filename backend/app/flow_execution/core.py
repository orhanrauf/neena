from datetime import datetime
import importlib
from typing import Any, Dict, List
from uuid import UUID

from app import crud, schemas
from app.db.session import SessionLocal
from app.flow_execution.integrations.base import BaseIntegration
from app.schemas.task_definition import TaskDefinition
from app.schemas.flow import Flow, FlowBase
from app.schemas.flow_run import FlowRun, FlowRunBase
from app.flow_execution.decorators import TaskResponse


class ExecutionContext:
    """
    The ExecutionContext class is responsible for running a flow and executing its tasks,
    as well as managing the stat of the flow run.
    """

    def __init__(self, user: schemas.User, flow: Flow):
        self.user = user
        self.flow = flow
        self.integrations_cache: Dict[UUID, BaseIntegration] = {}
        self.database = SessionLocal()
        self.path_to_integrations = "app.flow_execution.integrations"
        self.flow_run: FlowRun = None

    def _get_task_definition(self, task_definition_id: UUID) -> TaskDefinition:
        """
        Retrieves a task definition by its ID.
        """
        return crud.task_definition.get(self.database, task_definition_id)

    def _instantiate_flow_run(self, flow: FlowBase) -> FlowRun:
        """
        Instantiates a flow run for the given flow.
        Adds to self, writes to database, and returns the flow run object.
        """

        flow_run = FlowRunBase(
            flow=flow.id, status="in_progress", triggered_time=datetime.now(), triggered_by=self.user.email
        )

        self.flow_run = crud.flow_run.create(self.database, flow_run)

        return self.flow_run

    def _update_flow_run_status(self, status: str):
        """
        Updates the status of the flow run.
        """
        self.flow_run.status = status
        crud.flow_run.update(self.database, self.flow_run)

    def _update_flow_run_end_time(self):
        """
        Updates the end time of the flow run.
        """
        self.flow_run.end_time = datetime.now()
        crud.flow_run.update(self.database, self.flow_run)

    def get_integration_instance(self, integration_id: UUID) -> BaseIntegration:
        """
        Retrieves or creates an integration instance by its ID.
        """
        if integration_id in self.integrations_cache:
            return self.integrations_cache[integration_id]

        integration = schemas.Integration.from_orm(crud.integration.get(self.database, integration_id))

        path_to_integration = f"{self.path_to_integrations}.{integration.short_name}"

        module = importlib.import_module(path_to_integration)
        integration_class = getattr(module, integration.class_name)

        integration_instance = integration_class(self.user)
        self.integrations_cache[integration_id] = integration_instance
        return integration_instance

    def execute_task(self, task_definition: TaskDefinition, parameters: Dict[str,]) -> TaskResponse:
        """
        Executes a task based on its definition and provided parameters.
        """
        integration_instance = self.get_integration_instance(task_definition.integration)

        acutal_python_name = task_definition.python_method_name.split(".")[-1]
        method = getattr(integration_instance, acutal_python_name)

        return method(**parameters)

    def run_flow(self):
        """
        Executes all tasks in a flow. This is the main entry point for running a flow.

        This method does the following:
        1. Instantiates the flow run.
        2. Iterates over all tasks in the flow, interfacing with the integrations and
           TaskPreparationGenerator and updating the task run states as needed.
        3. Updates the flow run status to "completed" when all tasks have been executed successfully.
        """

        flow_run = self._instantiate_flow_run(self.flow)

        for task_op in flow.task_operations:
            task_definition = self._get_task_definition(task_op.task_definition)

            # Parse parameters from `input_yml` or another source as appropriate
            parameters = self.parse_parameters(task_definition.parameters)

            result = self.execute_task(task_definition, parameters)
            # Handle the result as needed

    def parse_parameters(self, parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parses task parameters from a given source.
        """
        pass
