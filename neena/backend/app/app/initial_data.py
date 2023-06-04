import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


def init() -> None:
    db = SessionLocal()
    init_db(db)


if __name__ == "__main__":
    main()
