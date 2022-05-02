from cmath import log
from datetime import datetime as dt
from typing import Dict, List
from app.model.data import Data
from app.model.sensor import Sensor
from app.model.user import User
from flask_bcrypt import check_password_hash
from sqlalchemy.sql import text
from flask_bcrypt import generate_password_hash
from app import Session, session
import yaml 
from copy import deepcopy
from app.dtos.measurement import Field, Measurement

# def auth_user(user: User):
def insert_data(body: Dict):
    with open('config/devices.yaml') as file:
        config = yaml.safe_load(file)
    
    application_id = body['applicationId']
    measurement_config = config[application_id]
    
    
    body_default = deepcopy(body)

    # Getting  values from config
    fields = measurement_config['values']
    types = measurement_config['types']
    values: List[Measurement] = []
    for item in fields:
        field = item['field']
        path = item['path']
        body_current = deepcopy(body_default)
        for key in path:    #iterating through incoming JSON to get path we want 
            body_current = body_current.get(key, {})
        # value = body_current[field]
        # additional_values.append({field: body_current[field]})
        values.append(Measurement(field, body_current[field], types[field]))
    #  -------------------------------------

    # Getting additional values from config
    timestamp_config = measurement_config['timestamp']
    timestamp_field = timestamp_config['field']
    timestamp_path = timestamp_config['path']
    for path in timestamp_path:
        body_default = body_default[path]
    
    # timestamp = body_default[timestamp_field]
    timestamp = dt.timestamp(dt.now())
    # ---------------------------------------
    print(f'timestamp: {timestamp}')
    # Getting Device data from config
    device_config = measurement_config['device']
    device_field = device_config['field']
    device_path = device_config['path']
    for key in device_path:
        body = body.get(key, {})
    
    device_id = body.get(device_field, None) #ID from received message 
    if not device_id:
        return {'ok': False, 'message': 'Device not found in recieved data'}

    print(device_id)
    # --------------------------------
    for measurement in values:
        print(measurement.fieldname, measurement.value)
    

    with Session.begin() as session:
        sensor: Sensor = session.query(Sensor).filter(Sensor.sensor == device_id).first()
        if not sensor:
            return {'ok': False, 'message': 'Device not found in database'}
        sensor_id = sensor.id
        measurements: List[Data] = []
        for measurement in values:
            print(measurement.fieldname, measurement.value)
            data: Data = Data(sensor_id=sensor_id, value=str(measurement.value), timestamp=timestamp, type_id=measurement.type_id)
            measurements.append(data)
        session.add_all(measurements)

    return {'ok': True, 'message': 'Data inserted to database'}


def create_user(user: User):
    pwd_hash = generate_password_hash(user.password).decode('utf-8')
    
    if pwd_hash:
        user.password = pwd_hash
    with Session.begin() as session:
        session.add(user)
        # session.commit()
    