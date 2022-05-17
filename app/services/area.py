from typing import Dict, List
from app import Session, session
from app.controller import user
from app.model.area import Area
from app.model.dtos.dtos import AreaWithSectorsDTO, SectorDTO
from app.model.sector import Sector

def get_all_user_areas(user_id: int):
    with Session.begin() as session:
        areas= session.query(Area).filter(Area.user_id==user_id).all()
    if not areas:
        return {"found": False, "message":"User has no areas"}, 404
    return {"found": True, "areas": [Area.serialize_area(area) for area in areas]}, 200


def get_areas_with_sectors(user_id: int):
    with Session.begin() as session:
        areas: List[Area] = session.query(Area).filter(Area.user_id == user_id).all()
    if not areas or len(areas) == 0:
        return {"status": False, "message":"User has no areas"}, 404 
    
    areas_with_sectors: List[AreaWithSectorsDTO] = []
    for area in areas:
        area_with_sector = AreaWithSectorsDTO(area.id, area.description)
        with Session.begin() as session:
            sectors: List[SectorDTO] = session.query(Sector).filter(Sector.area_id == area.id).all()
        if sectors and len(sectors) > 0:
            for sector in sectors:
                area_with_sector.sectors.append(SectorDTO(sector.id, sector.description))
        areas_with_sectors.append(area_with_sector)
    
    return {"status": True, "areas": [area.serialize() for area in areas_with_sectors] },200


#TO-DO get to know if user has yet area with that name .. 
# + two different users MAY have SAME area name(?)
def add_area(user_id: int, request_data: Dict):
    description = request_data["description"]

    area: Area = Area(description= description, user_id=user_id)
    with Session.begin() as session:
        session.add(area)
    if area.id:
        return {"ok": True, "message":"Area inserted", "id": area.id}, 201
    else:
        return {"ok": False, "message":f"Area: {description} could not be inserted"}, 500