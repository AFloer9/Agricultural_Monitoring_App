# Author: Alexander Flores Spring 2023 Class: CS 320

from datetime import datetime
from serial import Serial
from time import sleep

from sqlalchemy.orm import Session
import sqlalchmodels
from dbsetup import engine, get_db
from sqlalchemy import select, func


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
			sensor_id = 1,
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
		#print(max_value)
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


def getCurrentSensors(sensor_list, loc):
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
sensors = ["TEMP", "DHT_HUM", "DHT_TEMP"]#,"PHOTO", "MOIST", "WATER"] # having unneeded sensors messes up sensor_info @readData
data_points = 1
loc = 'backyard'
#readData(PORT, sensors, data_points, loc)


def show_sensor_data():
	with Session(engine) as session:
	
		#stmt = session.query(sqlalchmodels.SensorData.data_id, sqlalchmodels.SensorData.data, sqlalchmodels.SensorData.sensor_loc, func.strftime('%Y-%m-%d',sqlalchmodels.SensorData.date)).all()
		stmt = session.query(sqlalchmodels.Sensor.sensor_type, sqlalchmodels.SensorData.data, sqlalchmodels.SensorData.sensor_loc, func.strftime('%Y-%m-%d',sqlalchmodels.SensorData.date)).filter(sqlalchmodels.SensorData.data_id == sqlalchmodels.SensorRelation.data_id).filter(sqlalchmodels.SensorRelation.sensor_id == sqlalchmodels.Sensor.ID).all()
		return stmt

def show_sensors():
	with Session(engine) as session:
		return session.query(sqlalchmodels.Sensor.sensor_type, sqlalchmodels.Sensor.ID).all()

#print(show_sensor_data())
#show_sensor_data()
#print(show_sensors())
