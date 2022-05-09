from app.model.sensor import Sensor
from app import Session
from typing import Dict, List

from app.model.type import Type

def remove_sensor (body:Dict):
    sensor_id = body["sensorID"]
    with Session.begin() as session:
        sensorToDel= session.query(Sensor).filter(Sensor.id==sensor_id)
    if not sensorToDel:
        return {"ok":False, "message":"Device not found in database "} 
    
    with Session.begin() as session:
        session.delete(sensorToDel)
    
    with Session.begin() as session:
        isDeleted= session.query(Sensor).filter(Sensor.id==sensor_id)
    if not isDeleted:
        return {"ok":True, "message":"Sensor was deleted"}
    else: return{"ok":False, "message":"Something went wrong"}

#TO-DO think about what(paramaters) we need to add and to where(table)
# doesnt work  
def add_sensor(requested_data):
    sector_id= requested_data["sensor_id"]
    sensor= requested_data["sensor"]
    note= requested_data["note"]
    unit= requested_data["unit"]
    min_value= requested_data["min_value"]
    max_value= requested_data["max_value"]
    sensor_id= requested_data["sensor_id"]
    

    record_for_sensor_table: Sensor = Sensor(sector_id=sector_id, sensor=sensor)
    record_for_type_table: Type = Type(note=note, unit=unit, min_value=min_value, max_value=max_value, sensor_id=sensor_id)

    with Session.begin() as session:
        session.add(record_for_sensor_table)
        session.add(record_for_type_table)

    return {"ok":True, "message":"Sensor was added"}

  

    
