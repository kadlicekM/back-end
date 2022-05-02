from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, select, update, delete
from app import Base

class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    login = Column(String(20))
    password = Column(String(100))
    # name = Column(String(30))

    @staticmethod
    def serialize_login(user):
        return {'login': user.login, 'whatever': 'hello world !'}

    
    # @staticmethod
    # def deserialize(data):
    #     return User(name=data["name"], login=data["login"], password=data["password"])
    
    # @staticmethod
    # def auth(data):
    #     return User(login=data["login"], password=data["password"])
    
    @staticmethod
    def add(data):
        return User(login=data["login"], password=data["password"])