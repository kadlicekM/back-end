from app.model.sensor import Sensor
from app import Session
from typing import Dict, List

from app.model.sensor_type import SensorType

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
def add_sensor(request_data: Dict):
    sector_id= request_data["sector_id"]
    sensor= request_data["sensor"]
    sensor_types = request_data["sensor_types"]

    sensor_to_add: Sensor = Sensor(sector_id=sector_id, sensor=sensor)
    # record_for_type_table: Type = Type(note=note, unit=unit, min_value=min_value, max_value=max_value, sensor_id=sensor_id)

    with Session.begin() as session:
        session.add(sensor_to_add)
    if not sensor_to_add.id:
        return {"ok":False, "message":"Sensor: {sensor} could not be inserted."}, 500
    
    sensor_types_to_add: List[SensorType] = []
    for type_ in sensor_types:
        note= type_["note"]
        unit= type_["unit"]
        min_value= type_["min_value"]
        max_value= type_["max_value"]
        sensor_type= SensorType(note=note, unit=unit, min_value=min_value, max_value=max_value, sensor_id=sensor_to_add.id)
        sensor_types_to_add.append(sensor_type)
    with Session.begin() as session:
        session.add_all(sensor_types_to_add)
    if sensor_types_to_add:
        return {"ok":True, "id": sensor_to_add.id, "message": "Sensor: {} with all it's types: {} successfully inserted.".format(sensor, [e['note'] for e in sensor_types ])}, 200


def get_all_from_sector(sector_id: int):
    pass
