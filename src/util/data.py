import json
from typing import overload

class JSON:
    def __init__(self, path: str):
        self.path = path

    def get_data(self, key: str=None):
        with open(self.path, 'r', encoding="UTF-8") as jsonf:
            json_data = json.load(jsonf)

        if key == None:
            return json_data
        else:
            key_list = key.split('.')

            data = json_data
            for k in key_list:
                data = data[k]

            return data

    def set_data(self, key: str, obj: object, indent: int=4) -> None:
        key_list = key.split('.')

        with open(self.path, 'r', encoding="UTF-8") as jsonf:
            json_data = json.load(jsonf)

        data: dict = json_data
        for k in key_list:
            data = data[k]

        data.update(obj)

        with open(self.path, 'w', encoding="UTF-8") as jsonf:
            json.dump(data, jsonf, indent=indent)
