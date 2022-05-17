import uuid
from app.model.area import Area
from app.model.sector import Sector
from app.model.sensor import Sensor
from app import Session
from typing import Dict, List
from app.model.sensor_type import SensorType

def remove_sensor (body:Dict):
    sensor_id = body["sensorID"]
    with Session.begin() as session:
        sensorToDel= session.query(Sensor).filter(Sensor.id==sensor_id)
    if not sensorToDel:
        return {"ok": False, "message":"Device not found in database "}, 200
    
    with Session.begin() as session:
        session.delete(sensorToDel)
    
    with Session.begin() as session:
        isDeleted= session.query(Sensor).filter(Sensor.id==sensor_id)
    if not isDeleted:
        return {"ok": True, "message":"Sensor was deleted"}
    else: return{"ok": False, "message":"Something went wrong"}

def delete_sensor(body):
    sensor_id=body["id"]
    with Session.begin() as session:
        session.query(Sensor).filter(Sensor.id==sensor_id).delete()
    return {"ok":True, "message":"Senzor s id {sensor_id} je zmazaný"}, 200

#TO-DO think about what(paramaters) we need to add and to where(table)
# doesnt work  
def add_sensor(request_data: Dict):
    sector_id= request_data["sector_id"]
    sensor_name= request_data["sensor_name"]
    sensor_types = request_data["sensor_types"]
    while True:
        uid = uuid.uuid4()
        with Session.begin() as session:
            sensor_check: Sensor = session.query(Sensor).filter(Sensor.uid == uid).first()
        if not sensor_check:
            break
    sensor_to_add: Sensor = Sensor(sector_id=sector_id, sensor_name=sensor_name, uid=uid)
    # record_for_type_table: Type = Type(note=note, unit=unit, min_value=min_value, max_value=max_value, sensor_id=sensor_id)

    try:
        with Session.begin() as session:
            session.add(sensor_to_add)
    except Exception as e:
        return {"ok": False, "message": f"Sensor: {sensor_name} could not be inserted."}, 500
    
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
        return {"ok":True, "id": sensor_to_add.id, "uid": uid, "message": "Sensor: {} with all it's types: {} successfully inserted.".format(sensor_name, [e['note'] for e in sensor_types ])}, 200


def get_all_sensors_for_user(user_id: int):
    # print(user_id)
    with Session.begin() as session:
        users_areas: List[Area] = session.query(Area).filter(Area.user_id==user_id).all()
    if not users_areas:
        return {"ok": False, "message":"You have no areas available", "data": []}, 404
    # area_ids = [area.id for area in users_areas]
    areas = {area.id: area.description for area in users_areas} # 1:"house1" 2:"house2"
    # print(areas.keys())
    with Session.begin() as session:
        users_sectors: List[Sector] = session.query(Sector).filter(Sector.area_id.in_(areas.keys())).all() #arei id musí mať nejakú hodnotu z in_() ... ak má tak všetky takéto hodnoty vyhovujú filteru
    if not users_sectors:
        return {"ok": False, "message":"You have no sectors available", "data": []}, 404
    # sector_ids = [sector.id for sector in users_sectors]
    sectors = {sector.id: sector.description for sector in users_sectors}
    sector_areas = {sector.id: sector.area_id for sector in users_sectors}
    # print(sectors.keys())
    with Session.begin() as session:
        users_sensors: List[Sensor] = session.query(Sensor).filter(Sensor.sector_id.in_(sectors.keys())).all()
    if not users_sensors:
        return {"ok": False, "message":"You have no sensors available", "data": []}, 404
    sensor_ids = [sensor.id for sensor in users_sensors]
    
    # print(sensor_ids)
    with Session.begin() as session:
        sensor_types: List[SensorType] = session.query(SensorType).filter(SensorType.sensor_id.in_(sensor_ids)).all()
    # print([st.note for st in sensor_types])

    data = []
    for sensor in users_sensors:
        sensor_id = sensor.id
        obj = {
                # "id": sensor_id*sensor.sector_id*(sector_areas.get(sensor.sector_id, 1)), 
                "id_sensor": sensor_id, 
                "area": areas.get(sector_areas.get(sensor.sector_id, {}), 'N/A'), #N/A vráti keď nič nenájde v areách a prázdny objekt ked nič nenájde v sektoroch , aby to nepadlo 
                "sector": sectors.get(sensor.sector_id, 'N/A'),
                "sensor": sensor.sensor_name, 
                "sensor_types": []}
        # print([st.note for st in sensor_types])
        for sensor_type in sensor_types.copy():
            if not sensor_type.sensor_id == sensor_id:
                break
            st = sensor_types.pop(0) #nemá tu byť sensor_type?
            serialized_sensor_type = SensorType.serialize(st)
            obj["sensor_types"].append(serialized_sensor_type)

        data.append(obj)
    

    return {"ok": True, "data": data}, 200
