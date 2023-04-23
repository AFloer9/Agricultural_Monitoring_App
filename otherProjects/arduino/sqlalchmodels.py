# Author: Alexander Flores Spring 2023 Class: CS 320

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from dbsetup import Base


class Sensor(Base):
	__tablename__ = 'my_sensors'
	ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	sensor_type = Column(String, nullable=False)

	def __repr__(self):
		return f"{self.ID} {self.sensor_type}"

class SensorRelation(Base):
	__tablename__ = 'sensor_relation'
	sensor_id = Column(Integer, ForeignKey('my_sensors.ID'), primary_key=True, nullable=False)
	data_id = Column(Integer, ForeignKey('sensor_data.data_id'), primary_key=True, nullable=False)

	def __repr__(self):
		return f"{self.sensor_id} {self.data_id}"

class SensorData(Base):
	__tablename__ = 'sensor_data'
	date = Column(DateTime)
	data_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	data = Column(Float)
	sensor_loc = Column(String)

	def __repr__(self):
		return f"{self.data_id} {self.data} {self.sensor_loc} {self.date}"