
"""
This file contains a template for a local script that can be used to interact with the backend code.
"""

import sys
import os
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app import crud
from app.schemas.task_definition import TaskDefinition

# Assuming your .env file is in the current directory or specify the path
dotenv_path = '../../.env'

# Load or reload the .env file
load_dotenv(dotenv_path=dotenv_path)

# Add the backend directory to the sys.path to allow for absolute imports
sys.path.append(os.path.abspath('.'))

from app.core.config import settings

db = SessionLocal()

task_definitions = crud.task_definition.get_multi(db, skip=0, limit=100)

for task_def in task_definitions:
    task_definition_schema = TaskDefinition.from_orm(task_def)
    print(task_definition_schema.model_dump())


