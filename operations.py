import database as db
from functools import lru_cache
import logging

log = logging.getLogger(__name__)

@lru_cache
def get_db():
    db_obj = db.KeysDB()
    return db_obj


def set_value(key, value):
    db_obj = get_db()
    db_obj.dict[key] = value
    ret_value = f"Set {key} to {value}"
    return ret_value


def get_value(key, *args):
    db_obj = get_db()
    if key in db_obj.dict.keys():
        value = db_obj.dict[key]
        ret_value = f"Found {key} to have {value}"
    else:
        ret_value = f"No key {key} found"
    return ret_value


def del_value(key, *args):
    db_obj = get_db()
    if key in db_obj.dict.keys():
        del db_obj.dict[key]
        ret_value = f"Deleted {key} with {value}"
    else:
        ret_value = f"No key {key} found"
    return ret_value


operation_dict = {
    "set": set_value,
    "get": get_value,
    "del": del_value,
}


def execute(input):
    command, key, value = None, None, None
    if "get" in input:
        command, key = input.split(":")
    else:
        command, key, value = input.split(":")
    if command in operation_dict.keys():
        ret_value = operation_dict[command](key, value)
        log.info(ret_value)
        return ret_value
