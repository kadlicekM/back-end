from multiprocessing.sharedctypes import Value
from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey, create_engine, select, update, delete
from app import Base

class Data(Base):
    __tablename__ = 'data_table'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    value = Column(String(50))
    timestamp = Column(Integer)
    type_id = Column(Integer)


