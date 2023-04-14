# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Response, Request  # import library/framework
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from sqlalchemy.types import SchemaType, PickleType
from sqlalchemy import update, JSON, func
#import pydanticmodels
import sqlalchmodels  
from dbsetup import get_db, engine
from typing import Dict, Optional, List
import requests
import serial_data #Alex
from serial_data import getCurrentSensors

router = APIRouter()

templates = Jinja2Templates(directory="templates") #create template object for HTML

@router.get("/sensor_data")  #**Arduino data* list
def show_sensor_data():
	with Session(engine) as session:
		stmt = session.query(sqlalchmodels.SensorData).all()
		return stmt
		for row in stmt:
			print(row)
		print('')
		stmt = session.query(sqlalchmodels.SensorData.data_id, sqlalchmodels.SensorData.data, sqlalchmodels.SensorData.sensor_loc).all()
		for row in stmt:
			print(row)
	sensor_data = session.query(sqlalchmodels.SensorData).all()
	print(sensor_data)
    
@router.get("/my_sensors")  #LIST of all sensors
def show_sensors(db: Session = Depends(get_db)):
    seeds = db.query(sqlalchmodels.Sensor).all() 
    return seeds
    
@router.post("/my_sensors")  #ADD new sensor
def addSensor(sensorName):
	# maybe date sensor was added...  label is like look above maybe?
	with Session(engine) as session:
		result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		if not result:
			session.add(sqlalchmodels.Sensor(sensor_type = sensorName))
			session.commit()
			result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		return result[0][0]

@router.post("/sensor_data")            #ADD sensor data to database (from Arduino)
def addData(data_list, sensor_dict): # to db   
	with Session(engine) as session:
		#what if nothing
		max_value = session.query(func.max(sqlalchmodels.SensorData.data_id)).all()    #get list of all sensor data
		if not max_value:
			max_value = 0
		else:
			max_value = max_value[0][0]

		for row in data_list:
			max_value += 1
			sensor_info = sensor_dict[row[0]] # check if none

			sensorData = sqlalchmodels.SensorData(data_id = max_value, data = row[1], sensor_loc = sensor_info['loc'])
			sensorRelation = sqlalchmodels.SensorRelation(sensor_id = sensor_info['id'], data_id = max_value)
			
			session.add_all([sensorData, sensorRelation])
		
		session.commit()

#information = {'test_sensor':{'loc':'vancouver', 'id': 5}}     #TEST
#data_info = [['test_sensor', 1.3], ['test_sensor', 1.4], ['test_sensor', 1.5]]	#TEST
#addData(data_info, information)  #TEST


@router.get("/my_sensors") #LIST of all sensors
#def show_sensors(db: Session = Depends(get_db)):
    #sensors = db.query(sqlalchmodels.Sensor).all()
    #return sensors
def getCurrentSensors(sensor_list, loc):  #<<<<ALEX
	# returns dictionary of all the sensors with their ID
	# maybe insert loc somewhere else
	return {sensor:{'id':addSensor(sensor), 'loc':loc} for sensor in sensor_list}
    
    
#@router.get("/my_data")  #**Arduino data* list
#def show_sensor_data(db: Session = Depends(get_db)):
    #sensor_data = db.query(sqlalchmodels.SensorData).all()
    #return sensor_data
##Alex's version:
#def show_sensor_data():
	#with Session(engine) as session:
		#stmt = session.query(sqlalchmodels.SensorRelation).all()
		#for row in stmt:
			#print(row)