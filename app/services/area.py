from typing import Dict
from app import Session, session
from app.controller import user
from app.model.area import Area

def get_all_areas():
    # user_id= requested_data["user_id"]
    user_id = 14
    with Session.begin() as session:
        areas= session.query(Area).filter(Area.user_id==user_id).all()
    if not areas:
        return {"found": False, "message":"User has no areas"}, 404
    return {"found": True, "areas": [Area.serialize_area(area) for area in areas]},200

#TO-DO get to know if user has yet area with that name .. 
# + two different users MAY have SAME area name(?)
def add_area(requested_data):
    user_id = requested_data["user_id"]
    description = requested_data["description"]
    # with Session.begin() as session:
    #     area_to_compare:Dict= session.query(Area.user_id==user_id).all()
    #     print(area_to_compare)

    record: Area = Area(description= description, user_id=user_id)
    with Session.begin() as session:
        session.add(record)
    return {"ok":True, "message":"Area inserted"}
