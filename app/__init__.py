from re import fullmatch
from flask import Flask, jsonify
from flask.globals import request
from sqlalchemy.orm import Session, sessionmaker, registry
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, select, update, delete
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
#from sqlalchemy.sql.expression import except_

app = Flask(__name__)

CORS(app)
flask_bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] ='change_me'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

engine = create_engine(
    "mysql+pymysql://root:xsed2kj8@localhost:3306/diplomka_skuska")

Session = sessionmaker(bind=engine, future=True,expire_on_commit=False)
session = Session()
Base = declarative_base()