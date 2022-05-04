from multiprocessing.sharedctypes import Value
from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import VARCHAR, Table, Column, Integer, Float, String, ForeignKey, create_engine, select, update, delete
from app import Base

class Sector(Base):
    __tablename__ = 'sector_table'
    id = Column(Integer, primary_key=True)
    description = Column(VARCHAR)
    area_id = Column(Integer)
    #sensor = Column(String(45))

