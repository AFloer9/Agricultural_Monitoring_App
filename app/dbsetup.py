# slightly adapted from FastAPI documentation  https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_2_3  :
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"  # database URL

engine = create_engine(
    # allow multithread interactions for a single request:
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# make database session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # used to create ORM models later
