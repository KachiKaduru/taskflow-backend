from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

db_url = "sqlite:///./taskflow.db"

engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
