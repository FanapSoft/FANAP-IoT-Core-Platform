import jsonschema
import json
import os
from app.exception import ApiExp
import time


_json_schema_files = dict (
    user = 'schema_user_add.json',
    devicetype = 'schema_devicetype_add.json'
)


def json_validate(schema_name, data):
    payload_ok, payload_chk_msg = _validate(schema_name, data)

    if not payload_ok:
        raise ApiExp.Structural(dbg_msg=payload_chk_msg)
    return True

def _validate(schema_name, data):
    schema = schema_dict[schema_name]

    try:
        jsonschema.validate(data, schema)
        return (True, '')
    
    except jsonschema.ValidationError as e:
        return (False, e.message)


def _load_schema(filename):
    with open(filename , 'r') as f:
        schema = json.load(f)
    return schema


def create_schema_dict(filename_dict):
    ret = {}
    for name, fname in filename_dict.items():

        path = os.path.join(os.path.dirname(__file__), fname)

        ret[name] = _load_schema(path)
    return ret


schema_dict = create_schema_dict(_json_schema_files)