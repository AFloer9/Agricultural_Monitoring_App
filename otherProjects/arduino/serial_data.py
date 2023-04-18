# Author: Alexander Flores Spring 2023 Class: CS 320

from datetime import datetime
from serial import Serial
from time import sleep

from sqlalchemy.orm import Session
import sqlalchmodels
from dbsetup import engine, get_db
from sqlalchemy import select, func
#import pydanticmodels
#from pydantic import BaseModel


#sqlalchmodels.Base.metadata.drop_all(bind=engine)
sqlalchmodels.Base.metadata.create_all(bind=engine)


def insert_test_data():
	with Session(engine) as session:
		demo_sensorData = sqlalchmodels.SensorData(
			#date = datetime.now(),
			data = 1.0,
			sensor_loc = 'vancouver'
			)

		demo_sensor = sqlalchmodels.Sensor(
			ID = 5,
			sensor_type = 'test_sensor'
			)

		demo_sensorRelation = sqlalchmodels.SensorRelation(
			sensor_id = 5,
			data_id = 1
			)

		session.add_all([demo_sensorData, demo_sensorRelation, demo_sensor])
		session.commit()

#insert_test_data()


def addSensor(sensorName):
	# maybe date sensor was added...  label is like look above maybe?
	with Session(engine) as session:
		result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		if not result:
			session.add(sqlalchmodels.Sensor(sensor_type = sensorName))
			session.commit()
			result = session.query(sqlalchmodels.Sensor.ID).filter(sqlalchmodels.Sensor.sensor_type == sensorName).all()

		return result[0][0]

#print(addSensor('test_sensor'))
#print(addSensor('None_sensor'))


def addData(data_list, sensor_dict): # check what is returned when there is nothing in the db
	with Session(engine) as session:
		date = datetime.now()

		max_value = session.query(func.max(sqlalchmodels.SensorData.data_id)).all()
		print(max_value)
		if not max_value or max_value[0][0] == None:
			max_value = 0
		else:
			max_value = max_value[0][0]

		for row in data_list:
			max_value += 1
			sensor_info = sensor_dict[row[0]] # check if none

			sensorData = sqlalchmodels.SensorData(date = date, data_id = max_value, data = row[1], sensor_loc = sensor_info['loc'])
			sensorRelation = sqlalchmodels.SensorRelation(sensor_id = sensor_info['id'], data_id = max_value)
			
			session.add_all([sensorData, sensorRelation])
		
		session.commit()

# information = {'test_sensor':{'loc':'vancouver', 'id': 5}}
# data_info = [['test_sensor', 1.3], ['test_sensor', 1.4], ['test_sensor', 1.5]]
# addData(data_info, information)


def getDbData(attribute, constraints):
	pass


def getCurrentSensors(sensor_list, loc):
	# returns dictionary of all the sensors with their ID
	# maybe insert loc somewhere else
	return {sensor:{'id':addSensor(sensor), 'loc':loc} for sensor in sensor_list}


def readSensors(s, n):
	data = []

	i = 0
	while True:
		line = s.readline()
		if not line:
			#print(f"{i}. Didn't find anything")
			continue
		else:
			data.append(line.decode().strip().split()) # maybe split and put in a list
		i += 1
		if i == n:
			break
	
	print(data)
	print(f"Total: {i}")
	print('')

	return data


def readData(port, sensor_list, read_n_data, loc):
	with Serial(PORT, 9600, timeout=3) as s:
		#print(s.name)
		#print(s.readable())
		#print(s.get_settings())
		
		sensor_info = getCurrentSensors(sensor_list, loc)
		n = read_n_data * len(sensor_info) # number of data to read in (sensors are expected to run one after another)
		data = readSensors(s, n)
	
		addData(data, sensor_info)
		# store in db
	

PORT = 'COM5'
sensors = ["PHOTO", "MOIST", "TEMP", "DHT_HUM", "DHT_TEMP", "WATER"]
data_points = 5
loc = 'backyard'
#readData(PORT, sensors, data_points, loc)


def show_sensor_data():
	with Session(engine) as session:
		# stmt = session.query(sqlalchmodels.Sensor).all()
		
		# for row in stmt:
		# 	print(row)
		# print('')
		#stmt = session.query(sqlalchmodels.SensorData.date, sqlalchmodels.SensorData.data, sqlalchmodels.SensorData.sensor_loc).all()
		stmt = session.query(sqlalchmodels.SensorData.data, sqlalchmodels.SensorData.sensor_loc).all()
		return stmt
		# for row in stmt:
		# 	print(row)
	#sensor_data = db.query(sqlalchmodels.SensorData).all()
	#print(sensor_data)

#show_sensor_data()

# i = 0
# #sleep(3)
# while True:
# 	line = s.readline()
# 	if not line:
# 		# elif for strings that dont start with name of sensor
# 		print(f"{i}. Didn't find anything")
# 		continue
# 	else:
# 		print(f'{i}. {line.decode().strip()}')
# 	i += 1
# 	if i == 20:
# 		break
# print(f"Total: {i}")
# s.close()

