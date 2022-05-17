from typing import Dict
from app import Session, session
from app.model.sector import Sector

#TO-DO get to know if user has yet sector with that name ... 
# + two different users MAY have SAME sector name(?)
def add_sector(request_data: Dict):
    area_id= request_data["area_id"]
    description= request_data["description"]

    sector: Sector = Sector(description=description, area_id=area_id)
    with Session.begin() as session:
        session.add(sector)
    return {"ok":True, "message":"Sector inserted", "id": sector.id}, 201


def get_all_user_sectors(user_id: int):
    # Todo
    pass
    # with Session.begin() as session:
    #     areas= session.query(Area).filter(Area.user_id==user_id).all()
    # if not areas:
    #     return {"found": False, "message":"User has no areas"}, 404
    # return {"found": True, "areas": [Area.serialize_area(area) for area in areas]}, 200