from multiprocessing.sharedctypes import Value
from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import VARCHAR, Table, Column, Integer, Float, String, ForeignKey, create_engine, select, update, delete
from app import Base

class Area(Base):
    __tablename__ = 'area_table'
    id = Column(Integer, primary_key=True)
    description = Column(String(40))
    user_id = Column(Integer)
    #sensor = Column(String(45))

    @staticmethod
    def serialize_area(area):
        return {"description":area.description, "id": area.id}

    @staticmethod
    def customize_area(area):
        return {"description":area.description}
