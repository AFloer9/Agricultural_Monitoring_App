# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#ORM models--define database table attributes
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Sequence, Date, JSON, DateTime
#from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.sql.sqltypes import DATE
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from datetime import date
from dbsetup import Base  #Base class which all SQLalchemy models inherit from

# classes returned to user from API by http GET for reading
#each class below represents an object in the SQL database and it's columns (SQLALchemy)
class User(Base):  # extends class Base--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "users"
    # unique ID number for database
    #uid = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    # str = date.today()  # default = current date
    #join_date = Column(DATE, server_default=text('today()'))
    join_date = Column(String, nullable=False)
    pw = Column(String, nullable=False)
    email = Column(String, primary_key=True, nullable=False, unique=True)
    zipcode = Column(String)


class Seed(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "seedvault"
    id = Column(Integer, primary_key=True, nullable=False)
    seed_type = Column(String, nullable=False)
    coll_loc = Column(String) 
    coll_date = Column(String)
    num_coll = Column(Integer, default="1")  # int = "1"  # default = 1 seed


class Plant(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "my_plants"
    id = Column(Integer, primary_key=True, nullable=False)
    plant_type = Column(String(255), nullable=False)
    sci_name = Column(String(255))
    date_acq = Column(String(255))
    num_plants = Column(Integer, default="1")  # int = "1"  # default = 1 plant
    watering_week = Column(Integer, default="1")
    sunlight_hrs_day = Column(Integer, default="1")


class Supply(Base):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    __tablename__ = "my_supplies"
    id = Column(Integer, primary_key=True, nullable=False)
    supply_type = Column(String(255), nullable=False)
    brand_name = Column(String(255))
    purch_acq = Column(String(255))
    num_supply = Column(Integer, default="1")
    amt = Column(Integer, default="1")
    unit = Column(String(255), default="lbs")
    
#class ClimateData(Base): #weather data from APIs  ONLY NEED THIS CLASS IF STORED IN DB, else called directly
    #pred_rainfall = Column(Float)    
    #wind_speed = Column(Float)
    
###Alex's code>>>>
class Sensor(Base):
	__tablename__ = 'my_sensors'
	ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	sensor_type = Column(String, nullable=False)

	def __repr__(self):
		return f"{self.ID} {self.sensor_type}" #calls this object for print function

class SensorRelation(Base):
	__tablename__ = 'sensor_relation'
	sensor_id = Column(Integer, ForeignKey('my_sensors.ID'), primary_key=True, nullable=False)
	data_id = Column(Integer, ForeignKey('sensor_data.data_id'), primary_key=True, nullable=False)

	def __repr__(self):
		return f"{self.sensor_id} {self.data_id}" #calls this object for print function

class SensorData(Base):
	__tablename__ = 'sensor_data'
	date = Column(DateTime)
	data_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	data = Column(Float)
	sensor_loc = Column(String)