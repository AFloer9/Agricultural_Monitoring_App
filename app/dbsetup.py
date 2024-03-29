# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#SQLAlchemy database setup
# slightly adapted from FastAPI documentation  https://fastapi.tiangolo.com/tutorial/sql-databases/#__tabbed_2_3  :
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"  #name of .db file to comnect to

#fake demo SQL database(uncomment this OR the above line)
#SQLALCHEMY_DATABASE_URL = "sqlite:///./demo_database.db"

engine = create_engine(  #new database "factory"--manages connections to db
    # allow multithread interactions for a single request:
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
# make database session class--allows queries through SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # used to create ORM models later

# dependency--don't start a database session unless connected to DB:
def get_db():
    db = SessionLocal()  #session to send queries to endpoints/DB is created upon a request, closed out after 
    try:
        yield db
        print("connection to DB succeeded")  #DEBUG
    finally:
        db.close() #close connection to database
