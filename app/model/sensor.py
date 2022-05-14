from multiprocessing.sharedctypes import Value
from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, create_engine, select, update, delete
from app import Base

class Sensor(Base):
    __tablename__ = 'sensor_table'
    id = Column(Integer, primary_key=True)
    sector_id = Column(Integer)
    sensor_name = Column(String(45))
    uid = Column(String(100))


