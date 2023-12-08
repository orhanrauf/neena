from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
print("====="*30)
print("====="*30)
print(settings.SQLALCHEMY_DATABASE_URI)
print("====="*30)
print("====="*30)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
