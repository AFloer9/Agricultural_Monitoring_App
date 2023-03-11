#ORM models--define database table attributes
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.sql.sqltypes import DATE
from sqlalchemy.sql.expression import text

from dbsetup import Base

# classes returned to user from API by http GET for reading
#each class below represents an object in the SQL database and it's columns (SQLALchemy)
class User(Base):  # extends class Base--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "users"
    # unique ID number for database
    uid = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    # str = date.today()  # default = current date
    #join_date = Column(DATE, server_default=text('today()'))
    join_date = Column(String, nullable=False, default=date.today)
    pw = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    zipcode = Column(String, nullable=False)


class Seed(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "seedvault"
    id = Column(Integer, primary_key=True, nullable=False)
    seed_type = Column(String, nullable=False)
    coll_loc = Column(String)
    # str = date.today()  # default = current date
    coll_date = Column(String, nullable=False, default=date.today)
    num_coll = Column(Integer, default="1")  # int = "1"  # default = 1 seed


class Plant(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "my_plants"
    id = Column(Integer, primary_key=True, nullable=False)
    plant_type = Column(String, nullable=False)
    sci_name = Column(String)
    # str = date.today()  # default = current date
    date_acq = Column(String, nullable=False, default=date.today)
    num_plants = Column(Integer, default="1")  # int = "1"  # default = 1 plant
    watering_week = Column(Integer, default="1")
    sunlight_hrs_day = Column(Integer, default="1")


class Supply(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "my_supplies"
    id = Column(Integer, primary_key=True, nullable=False)
    supply_type = Column(String, nullable=False)
    brand_name = Column(String)
    # str = date.today()  # default = current date
    purch_acq = Column(String, nullable=False, default=date.today)
    # int = "1"  # default = 1 item/container
    num_supply = Column(Integer, nullable=False, default="1")
    # int = "1"  # default = 1 unit
    amt = Column(Integer, nullable=False, default="1")
    # str = "lbs."  # default = pounds; could be ounces, etc.
    unit = Column(String, nullable=False, default="lbs")
