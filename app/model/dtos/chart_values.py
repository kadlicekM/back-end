from typing import List, Union

class ChartObjectDTO():
    def __init__(self, sensor_type_id: int, note: str, unit: str, max, min):
        self.sensor_type_id = sensor_type_id
        self.note = note
        self.unit = unit
        self.max = max
        self.min = min
        self.values: List[ChartValueDTO] = []
        

    def serialize(self):
        return {'id': self.sensor_type_id, 'note': self.note, 'unit': self.unit, 'max': self.max, 'min': self.min, "values": [v.serialize() for v in self.values]}


class ChartValueDTO():
    def __init__(self, average: float, date_label_unix: str, date_label_dt ) -> None:
        self.average = average
        self.date_label_unix = date_label_unix
        self.date_label_dt = date_label_dt
        self.real_values: List[RealValueDTO] = []

    def serialize(self):
         return {'value': self.average, 'timestamp': self.date_label_unix, "date":self.date_label_dt, "real_values": [v.serialize() for v in self.real_values]}
        #  return {'value': self.average, 'timestamp': self.date_label_unix, "date":self.date_label_dt}


class RealValueDTO():
    def __init__(self, value: float, date_label: str) -> None:
        self.value = value
        self.date_label = date_label

    def serialize(self):
         return {'value': self.value, 'timestamp': self.date_label}