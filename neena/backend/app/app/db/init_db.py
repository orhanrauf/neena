from sqlalchemy import UUID
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.models.user import User

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db_task_definitions(db: Session, user: User) -> None:
  
    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="look_up_acc_number_by_email",
        parameters=[
            schemas.TaskParameter(
                name="email",
                data_type="str",
                position=0
            )
        ],
        output_type="str",
        output_name="acc_number",
        description="Looks up account number in the customer database by email.",
        python_code="@neena.task()\ndef look_up_acc_number_by_email(acc_number: str) -> str:\n    return db.select(f'SELECT * FROM dbo.Customers WHERE email={acc_number}')"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user)  # noqa: F841

    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="look_up_customer_detail_by_acc_number",
        parameters=[
            schemas.TaskParameter(
                name="detail_name",
                data_type="str",
                position=0
            ),
            schemas.TaskParameter(
                name="acc_number",
                data_type="str",
                position=1
            )
        ],
        output_type="str",
        output_name="customer_detail",
        description="Looks up a specific detail of a customer by account number.",
        python_code="@neena.task()\ndef look_up_customer_detail_by_acc_number(detail_name: str, acc_number: str) -> str:\n    return customer_db.get_customer_detail(detail_name, acc_number)"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841

    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="update_customer_address",
        parameters=[
            schemas.TaskParameter(
                name="customer_id",
                data_type="int",
                position=0
            ),
            schemas.TaskParameter(
                name="new_address",
                data_type="str",
                position=1
            )
        ],
        output_type="bool",
        output_name="success",
        description="Updates the address of a customer with the specified customer ID to the new address.",
        python_code="@neena.task()\ndef update_customer_address(customer_id: int, new_address: str) -> bool:\n    # Logic to update customer address\n    return success"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841


    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="process_return_request",
        parameters=[
            schemas.TaskParameter(
                name="order_id",
                data_type="str",
                position=0
            ),
            schemas.TaskParameter(
                name="reason",
                data_type="str",
                position=1
            )
        ],
        output_type="bool",
        output_name="success",
        description="Processes a return request for the specified order ID with the given reason.",
        python_code="@neena.task()\ndef process_return_request(order_id: str, reason: str) -> bool:\n    # Logic to process return request\n    return success"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841


    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="escalate_support_ticket",
        parameters=[
            schemas.TaskParameter(
                name="ticket_id",
                data_type="str",
                position=0
            ),
            schemas.TaskParameter(
                name="escalation_reason",
                data_type="str",
                position=1
            )
        ],
        output_type="bool",
        output_name="success",
        description="Escalates a support ticket with the specified ticket ID and provides the reason for escalation.",
        python_code="@neena.task()\ndef escalate_support_ticket(ticket_id: str, escalation_reason: str) -> bool:\n    # Logic to escalate support ticket\n    return success"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841


    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="send_notification_sms",
        parameters=[
            schemas.TaskParameter(
                name="phone_number",
                data_type="str",
                position=0
            ),
            schemas.TaskParameter(
                name="message",
                data_type="str",
                position=1
            )
        ],
        output_type="bool",
        output_name="success",
        description="Sends a notification SMS to the specified phone number with the given message.",
        python_code="@neena.task()\ndef send_notification_sms(phone_number: str, message: str) -> bool:\n    # Logic to send notification SMS\n    return success"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841


    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="update_profile",
        parameters=[
            schemas.TaskParameter(
                name="user_id",
                data_type="int",
                position=0
            ),
            schemas.TaskParameter(
                name="profile_data",
                data_type="dict",
                position=1
            )
        ],
        output_type="bool",
        output_name="success",
        description="Updates the profile of the user with the specified user ID using the provided profile data.",
        python_code="@neena.task()\ndef update_profile(user_id: int, profile_data: dict) -> bool:\n    # Logic to update user profile\n    return success"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841


    task_definition_in = schemas.TaskDefinitionCreate(
        task_name="calculate_total",
        parameters=[
            schemas.TaskParameter(
                name="items",
                data_type="list",
                position=0
            )
        ],
        output_type="float",
        output_name="total",
        description="Calculates the total cost based on the provided items.",
        python_code="@neena.task()\ndef calculate_total(items: list) -> float:\n    # Logic to calculate total\n    return total"
    )
    task_definition = crud.task_definition.create(db, obj_in=task_definition_in, current_user=user) # noqa: F841



def init_db_flow_request(db: Session) -> list[UUID]:
    flow_request_in = schemas.FlowRequestCreate(
        request_metadata={
            "city": "New York",
            "email": "johndoe@mail.com"
        },
        request_body="I would like to see if I am eligible for the discount given to customers in the Netherlands."
        
    )

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    
    

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        # Create user auth
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    
    init_db_task_definitions(db, user)
