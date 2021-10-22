import json
from typing import Union
from pathlib import Path


def read_json(path_to_json: Union[Path, str, object]) -> list:
    with open(path_to_json) as my_json:
        data = json.load(fp=my_json)
    return data


def write_json(path_to_json: Union[Path, str, object], data: list) -> None:
    with open(path_to_json, "w") as my_json:
        json.dump(obj=data, fp=my_json)
