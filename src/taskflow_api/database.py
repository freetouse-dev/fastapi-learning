from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from taskflow_api.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=({"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}),
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()