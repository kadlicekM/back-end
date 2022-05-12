from typing import List, Union

from app.model.data import Data


class Measurement():
    def __init__(self, fieldname: str, value: Union[str,int, float], type_id: int):
        self.fieldname = fieldname
        self.value = value
        self.type_id = type_id

class Field():
    def __init__(self, fieldname: str, value: Union[str,int, float]):
        self.fieldname = fieldname
        self.value = value


class ChartValue():
    def __init__(self, sensor_type_id: int, note: str, unit: str, max, min):
        self.sensor_type_id = sensor_type_id
        self.note = note
        self.unit = unit
        self.max = max
        self.min = min
        self.values: List[ValueInner] = []

    
    def serialize(self):
        return {'id': self.sensor_type_id, 'note': self.note, 'unit': self.unit, 'max': self.max, 'min': self.min, "values": [value.serialize() for value in self.values]}


class ValueInner():
    def __init__(self, average: float, date_label: str) -> None:
        self.average = average
        self.date_label = date_label

    def serialize(self):
         return {'value': self.average, 'timestamp': self.date_label}