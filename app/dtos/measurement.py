from typing import Union


class Measurement():
    def __init__(self, fieldname: str, value: Union[str,int, float], type_id: int):
        self.fieldname = fieldname
        self.value = value
        self.type_id = type_id

class Field():
    def __init__(self, fieldname: str, value: Union[str,int, float]):
        self.fieldname = fieldname
        self.value = value