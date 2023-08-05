import logging

from app.db.init_db import init_db
from app.execution.sync import update_task_definitions_from_directory
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    update_task_definitions_from_directory("app/task_definitions/", db)
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
