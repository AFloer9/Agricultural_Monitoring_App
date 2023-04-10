from serial import Serial
from time import sleep

from datetime import date
from sqlalchemy.orm import Session
import sqlalchmodels
from dbsetup import engine, get_db
from sqlalchemy import select, func
#import pydanticmodels
#from pydantic import BaseModel

PORT = 'COM5'
#s = Serial(PORT, 9600, timeout=3)
#print(s.name)
#print(s.readable())
#print(s.get_settings())

sqlalchmodels.Base.metadata.drop_all(bind=engine)
sqlalchmodels.Base.metadata.create_all(bind=engine)

# database libs you are using  ** what should i install maybe how to insert
# should we do some networking?

def insert_test_data():
	with Session(engine) as session:
		demo_sensorData = sqlalchmodels.SensorData(
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

insert_test_data()

#sensors = ["PHOTO", "MOIST", "TEMP", "DHT_HUM", "DHT_TEMP", "WATER"]


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

def addData(data_list, sensor_dict): # to db
	with Session(engine) as session:
		#what if nothing
		max_value = session.query(func.max(sqlalchmodels.SensorData.data_id)).all()
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

#information = {'test_sensor':{'loc':'vancouver', 'id': 5}}
#data_info = [['test_sensor', 1.3], ['test_sensor', 1.4], ['test_sensor', 1.5]]
#addData(data_info, information)

def getDbData(attribute, constraints):
	pass

def getCurrentSensors():
	# maybe readData takes in the sensors that will be used
	# like structure '<name of sensor> <data>'
	# at end tell what data was ignored and how much was recorded
	pass

def readData(port):
	# maybe how much i should read param?

	# make sure data is readable
	#print(s.readable())

	# return list or store in db
	pass


def show_sensor_data():
	with Session(engine) as session:
		stmt = session.query(sqlalchmodels.SensorRelation).all()
		
		for row in stmt:
			print(row)
	#sensor_data = db.query(sqlalchmodels.SensorData).all()
	#print(sensor_data)

show_sensor_data()

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

