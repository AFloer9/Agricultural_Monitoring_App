# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#SCHEMAS--structure requests--allows auto-validation of user data adherence to format
from pydantic import BaseModel, EmailStr, Field
from datetime import date  # for default today's date insertion to date fields
from typing import Optional, Dict

#BASELINE SCHEMAS--for HTTP GET all
class User(BaseModel):  #for HTTP GET  extends class BaseModel
    #uid: int  # unique ID number for database
    name: str
    user_name: str
    join_date: date = date.today()  # default = current date
    pw: str
    email: EmailStr #ensures valid email format
    zipcode: int
    class Config:       #makes Pydantic model compatible with ORM (SQLAlchemy)--converts
        orm_mode = True     #makes models include relationship data when returned from pathop


class Seed(BaseModel):
    id: int
    seed_type: str
    coll_loc: str
    coll_date: date #= date.today() # default = current date #format: YYYY-M-D
    num_coll: int = 1  # default = 1 seed
    class Config:
        orm_mode = True


class Plant(BaseModel):  
    id: int
    plant_type: str
    sci_name: str
    date_acq: date = date.today()  # default = current date
    num_plants: int = 1  # default = 1 plant
    watering_week: int
    sunlight_hrs_day: int
    class Config:
        orm_mode = True

class Supply(BaseModel):  
    id: int
    supply_type: str
    brand_name: str
    purch_acq: date = date.today()  # default = current date
    num_supply: int = 1  # default = 1 item/container
    amt: int = 1  # default = 1 unit
    unit: str = "lbs."  # default = pounds; could be ounces, etc.
    class Config:
        orm_mode = True
        
class Sensor(BaseModel): #user's sensors
    id: int
    sensor_type: str
    brand_name: str
    sensor_loc: str
    voltage : float
    class Config:
        orm_mode = True
        
class SensorData(BaseModel):
    id: int
    data_type: str  #water level, humidity, shade, temperature
    data_coll_date: date = date.today()  # default = current datestr
    unit: str   #percent, Fahrenheit
    reading: float
    class Config:
        orm_mode = True
        
class ClimateData(BaseModel): #weather data from APIs--called directly
    temperature: float
    pred_rainfall: float 
    wind_speed: float
    dewpoint: float
    short_cast: str
    det_cast: str
    class Config:       
        orm_mode = True

    
    
    
# CREATION SCHEMAS--inherit all attributes except ID from baseline schemas--for HTTP POST
class CreateUser(BaseModel): 
    name: str
    user_name: str
    join_date: date = date.today()  # default = current date
    pw: str
    email: EmailStr 
    zipcode: int
    class Config:       
        orm_mode = True
    
class ReturnUser(User):
    uid: int
    name: str
    user_name: str
    join_date: date = date.today()  # default = current date
    email: EmailStr 
    zipcode: int
    class Config:       
        orm_mode = True

class CreateSeed(Seed): 
    id: Optional[int] #seed id inserted according to DB index
    seed_type: str
    coll_loc: str
    coll_date: date = date.today()  # default = current date
    num_coll: int = 1  # default = 1 seed
    class Config:       
        orm_mode = True

class CreatePlant(Plant):  
    plant_type: str
    sci_name: str
    date_acq: date = date.today()  # default = current date
    num_plants: int = 1  # default = 1 plant
    watering_week: int
    sunlight_hrs_day: int
    class Config:       
        orm_mode = True


class CreateSupply(Supply):  
    supply_type: str
    brand_name: str
    purch_acq: date = date.today()  # default = current date
    num_supply: int = 1  # default = 1 item/container
    amt: int = 1  # default = 1 unit
    unit: str = "lbs."  # default = pounds; could be ounces, etc.
    class Config:       
        orm_mode = True
    
class CreateSensor(Sensor): 
    sensor_type: str
    brand_name: str
    sensor_loc: str
    voltage : float
    class Config:       
        orm_mode = True

#EDIT/UPDATE schemas: inherit SOME attributes from baseline classes--FOR HTTP PUT
class EditUser(User): 
    name: str
    user_name: str
    email: str
    zipcode: int
    class Config:       
        orm_mode = True

#class EditSeed(BaseModel):  
class EditSeed(Seed):  
    id: int
    seed_type: str
    coll_loc: str
    coll_date: date #= date.today()  # default = current date
    num_coll: int = 1  # default = 1 seed
    class Config:       
        orm_mode = True

class EditPlant(Plant):  
    plant_type: str
    sci_name: str
    date_acq: date = date.today()  # default = current date
    num_plants: int = 1  # default = 1 plant
    watering_week: int
    sunlight_hrs_day: int
    class Config:       
        orm_mode = True

class EditSupply(Supply):  
    supply_type: str
    brand_name: str
    purch_acq: date = date.today()  # default = current date
    num_supply: int = 1  # default = 1 item/container
    amt: int = 1  # default = 1 unit
    unit: str = "lbs."  # default = pounds; could be ounces, etc.
    class Config:       
        orm_mode = True
    
class EditSensor(Sensor): 
    sensor_type: str
    brand_name: str
    sensor_loc: str
    voltage : float
    class Config:       
        orm_mode = True

#deletion schemas: inherit SOME attributes from baseline classes--for HTTP DELETE

class DeleteUser(User):  #inherits all attributes from class User
    pass

class DeleteSeed(Seed):  #inherits all attributes from class Seed
    pass

class DeletePlant(Plant):  #inherits all attributes from class Plant
    pass

class DeleteSupply(Supply):  #inherits all attributes from class Supply
    pass

class DeleteSensor(Sensor):
    pass