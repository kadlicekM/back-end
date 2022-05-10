from typing import Dict
from app import Session, session
from app.model.sector import Sector

def get_areas_sectors():
    # user_id= requested_data["user_id"]
    area_id = 1
    with Session.begin() as session:
        sectors= session.query(Sector).filter(Sector.area_id==area_id).all()
    if not sectors:
        return {"found": False, "message":"User has no areas"}, 404
    return {"found": True, "sectors": [Sector.serialize_sector(sector) for sector in sectors] },200

#TO-DO get to know if user has yet sector with that name ... 
# + two different users MAY have SAME sector name(?)
def add_sector(request_data: Dict):
    area_id= request_data["area_id"]
    description= request_data["description"]

    sector: Sector = Sector(description=description, area_id=area_id)
    with Session.begin() as session:
        session.add(sector)
    return {"ok":True, "message":"Sector inserted", "id": sector.id}, 201