from multiprocessing.sharedctypes import Value
from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import VARCHAR, Table, Column, Integer, Float, String, ForeignKey, create_engine, select, update, delete
from app import Base

class SensorType(Base):
    __tablename__ = 'type_table'
    id = Column(Integer, primary_key=True)
    note = Column(VARCHAR(45))
    unit = Column(VARCHAR(20))
    min_value = Column(Integer)
    max_value = Column(Integer)
    sensor_id = Column(Integer)
    

    @staticmethod
    def serialize(sensor_type):
        return {'id': sensor_type.id, 
                'note': sensor_type.note,
                "unit": sensor_type.unit,
                "max_value": sensor_type.max_value,
                "min_value": sensor_type.min_value}
