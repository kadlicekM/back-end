class AreaWithSectorsDTO():
    def __init__(self, area_id: id, area_description: str) -> None:
        self.area_id = area_id
        self.area_description = area_description
        self.sectors = []
    

    def serialize(self):
         return {'id': self.area_id, 'descritpion': self.area_description, 'sectors': [sector.serialize() for sector in self.sectors] }


class SectorDTO():
    def __init__(self, sector_id: id, sector_description: str) -> None:
        self.sector_id = sector_id
        self.sector_description = sector_description
    

    def serialize(self):
         return {'id': self.sector_id, 'descritpion': self.sector_description}