from cmath import log
from datetime import time, timedelta, datetime as dt
from operator import and_
from random import randint, random
from typing import Dict, List
from app.model.data import Data
from app.model.sensor import Sensor
from app.model.sensor_type import SensorType
from app.model.user import User
from flask_bcrypt import check_password_hash
from sqlalchemy.sql import text
from flask_bcrypt import generate_password_hash
from app import Session, session
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import yaml 
from copy import deepcopy
from app.model.dtos.chart_values import ChartObjectDTO, RealValueDTO, ChartValueDTO

# def auth_user(user: User):
# def insert_data(body: Dict):
#     with open('config/devices.yaml') as file:
#         config = yaml.safe_load(file)
    
#     application_id = body['applicationId']
#     measurement_config = config[application_id]
    
    
#     body_default = deepcopy(body)

#     # Getting  values from config
#     fields = measurement_config['values']
#     types = measurement_config['types']
#     values: List[Measurement] = []
#     for item in fields:
#         field = item['field']
#         path = item['path']
#         body_current = deepcopy(body_default)
#         for key in path:    #iterating through incoming JSON to get path we want 
#             body_current = body_current.get(key, {})
#         # value = body_current[field]
#         # additional_values.append({field: body_current[field]})
#         values.append(Measurement(field, body_current[field], types[field]))
#     #  -------------------------------------

#     # Getting additional values from config
#     timestamp_config = measurement_config['timestamp']
#     timestamp_field = timestamp_config['field']
#     timestamp_path = timestamp_config['path']
#     for path in timestamp_path:
#         body_default = body_default[path]
    
#     # timestamp = body_default[timestamp_field]
#     timestamp = dt.timestamp(dt.now())
#     # ---------------------------------------
#     print(f'timestamp: {timestamp}')
#     # Getting Device data from config
#     device_config = measurement_config['device']
#     device_field = device_config['field']
#     device_path = device_config['path']
#     for key in device_path:
#         body = body.get(key, {})
    
#     device_id = body.get(device_field, None) #ID from received message 
#     if not device_id:
#         return {'ok': False, 'message': 'Device not found in recieved data'}, 404

#     print(device_id)
#     # --------------------------------
#     for measurement in values:
#         print(measurement.fieldname, measurement.value)
    

#     with Session.begin() as session:
#     #     sensor: Sensor = session.query(Sensor).filter(Sensor.id == device_id).first()
#     #     if not sensor:
#     #         return {'ok': False, 'message': 'Device not found in database'}
#     #     sensor_id = sensor.id
#         measurements: List[Data] = []
#         for i in range(10):
#             for j in range(24):
#                 tm = dt.now().replace(hour=j, minute=0, second=0, microsecond=0) - timedelta(days=i)
#                 timestmp = tm.timestamp()
#                 for measurement in values:
#                     print(measurement.fieldname, measurement.value)
#                     data: Data = Data(value=float(randint(1, 60)), timestamp=timestmp, type_id=measurement.type_id)
#                     # data: Data = Data(value=float(measurement.value), timestamp=timestmp, type_id=measurement.type_id)
#                     measurements.append(data)
#         session.add_all(measurements)

#     return {'ok': True, 'message': 'Data inserted to database'}, 200



def add_data(request_data: Dict):
    uid = request_data['uid'] if 'uid' in request_data else None
    if not uid:
        return {'ok': False, 'message': '"uid" attribute is missing in recieved data, could not be inserted.'}, 400
    with Session.begin() as session:
        sensor: Sensor = session.query(Sensor).filter(Sensor.uid == uid).first()
    if not sensor.id:
        return {'ok': False, 'message': f'Could not find sensor for specified uid: {uid}, data could not be inserted.'}, 400
    with Session.begin() as session:
        sensor_types: List[SensorType] = session.query(SensorType).filter(SensorType.sensor_id == sensor.id).all()
    if not sensor_types or not isinstance(sensor_types, list) or len(sensor_types) == 0:
        return {'ok': False, 'message': f'Could not find any sensor types for specified sensor: {sensor.sensor_name}, with uid: {sensor.uid}, data could not be inserted.'}, 400
    
    sensor_types_dict = {st.note: st.id for st in sensor_types}
    # Everything went well...
    data = request_data['data'] if 'data' in request_data else None
    if not data:
        return {'ok': False, 'message': '"data" attribute is missing in recieved data, could not be inserted.'}, 400
    
    
    with Session.begin() as session:
        for i in range(1):
            for j in range(24):
                tm = dt.now().replace(hour=j, minute=0, second=0, microsecond=0) - timedelta(days=i)
                timestmp = tm.timestamp()
                print(tm)
                for st in sensor_types:
                    data: Data = Data(value=float(randint(1, 60)), timestamp=timestmp, type_id=st.id)
                    session.add(data)
    
    return {'ok': True, 'message': 'Data inserted to database'}, 200

    
    # measurements: List[Measurement] = []
    # with Session.begin() as session:
    #     for obj in data:
    #         type_id = sensor_types_dict.pop(obj['type'], None)
    #         if type_id:
    #             measurements.append(Measurement(uid, type_id, obj['type'], obj['value'], obj['timestamp']))
    #             session.add(Data(type_id= type_id, value=obj['value'], timestamp=obj['timestamp']))
    # if measurements:
    #     return {'ok': True, 'message': 'Data inserted to database', 'data': [e.serialize() for e in measurements]}, 200
    


def get_chart_data(request_data: Dict):
    intervals = {'hour': timedelta(hours=1), 'day': timedelta(days=1), 'week': timedelta(weeks=1), 'month': relativedelta(month=1), 'year': relativedelta(year=1)}
    interval = request_data['interval']
    if interval not in intervals.keys():
        return {'status': False, 'message': 'Wrongly specified "interval" request parameter', 'data': []}, 400
    
    range_from = request_data['from'] # date in string fmt
    range_to = request_data['to']   #string

    timestamp_from = parse(range_from)#.timestamp() #miki može poslat dátum v hociakom formáte , fkc parse ho rozpozná a preloží do datetime python objektu
    timestamp_to = parse(range_to)#.timestamp()
    temp_timestamp_from = timestamp_from
    
    date_intervals = []
    while temp_timestamp_from < timestamp_to:
        if temp_timestamp_from + intervals.get(interval) <= timestamp_to:
            temp_timestamp_to = temp_timestamp_from + intervals.get(interval)
            date_intervals.append({'from': temp_timestamp_from, 'to': temp_timestamp_to})
            # temp_timestamp_from = temp_timestamp_from + intervals.get(interval)
            temp_timestamp_from = temp_timestamp_to
        else:
            # temp_timestamp_to = timestamp_to
            date_intervals.append({'from': temp_timestamp_from, 'to': timestamp_to})
            break
        
    print(date_intervals)
    # return {'status': False, 'message': 'Wrongly specified "interval" request parameter', 'data': date_intervals}, 200

     # enum(dd, w, m, y)
    # sensor_id = request_data['sensor_id']
    #store  list(pole) of sensor_type_ids if something is in the  
    sensor_type_ids = request_data['sensor_type_ids'] if 'sensor_type_ids' in request_data and isinstance(request_data['sensor_type_ids'], list) and len(request_data['sensor_type_ids']) > 0 else None
    
    with Session.begin() as session:
        # sensor_types: List[SensorType] = session.query(SensorType).filter(SensorType.sensor_id == sensor_id if not sensor_type_ids else SensorType.id.in_(sensor_type_ids)).all()
        sensor_types: List[SensorType] = session.query(SensorType).filter(SensorType.id.in_(sensor_type_ids)).all()
    if not sensor_types or len(sensor_types) == 0:
        return {'status': False, 'message': 'No sensor types found for selected sensor!', 'data': []}, 404
    # sensor_type_ids = [st.id for st in sensor_types]
    sensor_types_measurements: List[ChartObjectDTO] = []
    for sensor_type in sensor_types:
        chart_value = ChartObjectDTO(sensor_type.id, sensor_type.note, sensor_type.unit, sensor_type.max_value, sensor_type.min_value)
        values: List[Dict] = []
        # ! Todo need to put DB query in for loop for each date interval divided into batches of dates from: range_from = request_data['from'] to: range_to = request_data['to']
        for date in date_intervals:
            print(date) 
            with Session.begin() as session:
                sensor_type_values: List[Data] = session.query(Data).filter(and_(and_(Data.timestamp >= date['from'].timestamp(), Data.timestamp <= date['to'].timestamp()), Data.type_id == sensor_type.id)).order_by(Data.timestamp.asc()).all()
            # print(len(sensor_type_values))
            if sensor_type_values and len(sensor_type_values) > 0:
                average = round(sum([v.value for v in sensor_type_values])/len(sensor_type_values), 2) #searching through value in data object- sensor_type_values
            else:
                average = 0
            
            date_label_dt = date['from']
            date_label_unix = dt.timestamp(date_label_dt) #malo by spraviť s pekného datetime objektu unix timestamp 
            value = ChartValueDTO(average, date_label_unix,date_label_dt)
            for real_value in sensor_type_values:
                value.real_values.append(RealValueDTO(real_value.value, dt.fromtimestamp(real_value.timestamp).isoformat()))
            
            values.append(value)
        chart_value.values = values
        sensor_types_measurements.append(chart_value)
    
    return {'status': True, 'data': [e.serialize() for e in sensor_types_measurements]}, 200