from typing import List, Union

class ChartObject():
    def __init__(self, sensor_type_id: int, note: str, unit: str, max, min):
        self.sensor_type_id = sensor_type_id
        self.note = note
        self.unit = unit
        self.max = max
        self.min = min
        self.values: List[ChartValue] = []
        

    def serialize(self):
        return {'id': self.sensor_type_id, 'note': self.note, 'unit': self.unit, 'max': self.max, 'min': self.min, "values": [v.serialize() for v in self.values]}


class ChartValue():
    def __init__(self, average: float, date_label: str) -> None:
        self.average = average
        self.date_label = date_label
        self.real_values: List[RealValue] = []

    def serialize(self):
        #  return {'value': self.average, 'timestamp': self.date_label, "real_values": [v.serialize() for v in self.real_values]}
         return {'value': self.average, 'timestamp': self.date_label}


class RealValue():
    def __init__(self, value: float, date_label: str) -> None:
        self.value = value
        self.date_label = date_label

    def serialize(self):
         return {'value': self.value, 'timestamp': self.date_label}