from datetime import datetime
import json
import os
from os import path

_root_path = path.join(path.dirname(__file__), "..")

def get_root_path():
    return _root_path

def get_current_datetime():
    return datetime.now()

def get_current_datetime_str():
    return get_current_datetime().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date_str():
    return get_current_datetime().strftime("%Y-%m-%d")

def create_if_not_exists(file_path: str):
    no_file_path = path.dirname(file_path)
    if not path.exists(no_file_path):
        os.makedirs(no_file_path)

def load_json(relative_path: str):
    file_path = path.join(get_root_path(), relative_path)
    if not path.exists(file_path):
        with open(file_path, "a") as file:
            file.write("{\n\n}")
    content = {}
    with open(file_path, "r") as file:
        content = json.load(file)
    return content

def update_json(relative_path: str, new_content: dict):
    file_path = path.join(get_root_path(), relative_path)
    if not path.exists(file_path):
        with open(file_path, "a") as file:
            file.write("{\n\n}")
    
    content = {}
    with open(file_path, "w") as file:
        json.dump(new_content, file)

def get_version():
    v= "0.0.0"
    with open(path.join(get_root_path(), "../VERSION.txt")) as file:
        v = file.read().strip()
    return v