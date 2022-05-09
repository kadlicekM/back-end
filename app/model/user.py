from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import Boolean, Table, Column, Integer, String, ForeignKey, create_engine, select, update, delete
from app import Base

class User(Base):
    __tablename__ = 'user_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    surname = Column(String(20))
    login = Column(String(20))
    password = Column(String(100))
    email = Column(String(100))
    active = Column(Boolean)
    role = Column(String(20))
    user_token = Column(String(100))
    
    
    
    # name = Column(String(30))

    @staticmethod
    def serialize_token_payload(user):
        return {'login': user.login, 'id': user.id,"user_token":user.user_token if user.user_token else ""}
    
    @staticmethod
    def serialize_user(user):
        return {'id': user.id, 'login': user.login, 'active': user.active, 'email': user.email}

    
    # @staticmethod
    # def deserialize(data):
    #     return User(name=data["name"], login=data["login"], password=data["password"])
    
    # @staticmethod
    # def auth(data):
    #     return User(login=data["login"], password=data["password"])
    
    @staticmethod
    def add(data):
        return User(login=data["login"], password=data["password"])

        
