# Author: Anna Hyer  & Alex Flores Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Response, Request  # import library/framework
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from sqlalchemy import update, JSON, func
import sqlalchmodels
import dbsetup
from typing import Dict, Optional, List
import serial

router = APIRouter()

templates = Jinja2Templates(directory="./templates") #create template object for HTML

@router.get("/")
def show_sensor_data(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/sensor_data")  #**Arduino data* list #ALEX
def show_sensor_data2():
	with Session(dbsetup.engine) as session:
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
def show_sensors(request: Request, db: Session = Depends(dbsetup.get_db)):
    sensors = db.query(sqlalchmodels.Sensor).all() 
    return sensors
    #return templates.TemplateResponse("index.html", {"request": request, "sensors": sensors})
    
@router.post("/my_sensors/{sensorName}")  #ADD new sensor
def addSensor(sensorName):  #ALEX
	# maybe date sensor was added...  label is like look above maybe?
	with Session(dbsetup.engine) as session:
		result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		if not result:      #if a sensor with this name is not found
			session.add(sqlalchmodels.Sensor(sensor_type = sensorName))
			session.commit()
			result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		return result[0][0]     #return ID of sensors with this name

# @router.post("/sensor_data")            #ADD sensor data to database (from Arduino)
# def addData(data_list, sensor_dict): # to db   #ALEX
# 	with Session(engine) as session:
# 		#what if nothing
# 		max_value = session.query(func.max(sqlalchmodels.SensorData.data_id)).all()    #get list of all sensor data
# 		if not max_value:
# 			max_value = 0
# 		else:
# 			max_value = max_value[0][0]

# 		for row in data_list:
# 			max_value += 1
# 			sensor_info = sensor_dict[row[0]] # check if none

# 			sensorData = sqlalchmodels.SensorData(data_id = max_value, data = row[1], sensor_loc = sensor_info['loc'])
# 			sensorRelation = sqlalchmodels.SensorRelation(sensor_id = sensor_info['id'], data_id = max_value)
			
# 			session.add_all([sensorData, sensorRelation])
		
# 		session.commit()

# information = {'test_sensor':{'loc':'vancouver', 'id': 5}}     #TEST
# data_info = [['test_sensor', 1.3], ['test_sensor', 1.4], ['test_sensor', 1.5]]	#TEST
# addData(data_info, information)  #TEST


@router.get("/my_sensors") #LIST of all sensors
#def show_sensors(db: Session = Depends(get_db)):
    #sensors = db.query(sqlalchmodels.Sensor).all()
    #return sensors
def getCurrentSensors(sensor_list, loc):  #ALEX
	# returns dictionary of all the sensors with their ID
	# maybe insert loc somewhere else
	return {sensor:{'id':addSensor(sensor), 'loc':loc} for sensor in sensor_list}
    
    
#@router.get("/sensor_data")  #**Arduino data* list
#def show_sensor_data(db: Session = Depends(get_db)):
    #sensor_data = db.query(sqlalchmodels.SensorData).all()
    #return sensor_data
##Alex's version:
#def show_sensor_data():
	#with Session(engine) as session:
		#stmt = session.query(sqlalchmodels.SensorRelation).all()
		#for row in stmt:
			#print(row)