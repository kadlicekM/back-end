from typing import Dict
from app import Session, session
from app.controller import user
from app.model.area import Area

def get_all_areas(user_id: int):
    with Session.begin() as session:
        areas= session.query(Area).filter(Area.user_id==user_id).all()
    if not areas:
        return {"found": False, "message":"User has no areas"}, 404
    return {"found": True, "areas": [Area.serialize_area(area) for area in areas]}, 200

#TO-DO get to know if user has yet area with that name .. 
# + two different users MAY have SAME area name(?)
def add_area(user_id: int, request_data: Dict):
    description = request_data["description"]

    area: Area = Area(description= description, user_id=user_id)
    with Session.begin() as session:
        session.add(area)
    if area.id:
        print('here')
        return {"ok": True, "message":"Area inserted", "id": area.id}, 201
    else:
        return {"ok": False, "message":"Area: {description} could not be inserted"}, 500