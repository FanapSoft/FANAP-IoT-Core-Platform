import jsonschema
import json
import os
from app.exception import ApiExp
from flask import request


_json_schema_files = dict(
    user='schema_user_add.json',
    devicetype='schema_devicetype_add.json',
    device='schema_device_add.json',
    device_edit='schema_device_edit.json',
    role_add='schema_role_add.json',
    role_update='schema_role_update.json',
    role_grant='schema_role_grant.json',
    devicedata_write='schema_devicedata_write.json',
)


def json_validate(schema_name, data):
    payload_ok, payload_chk_msg = _validate(schema_name, data)

    if not payload_ok:
        raise ApiExp.Structural(dbg_msg=payload_chk_msg)
    return True


def check_uniqe_filed_in_list(schema, data):
    _chk = schema.get('__uniqe_field_check', '')

    if not _chk:
        return (True, '')

    fields_for_check = _chk if type(_chk) in [list, tuple] else [_chk]

    for f in fields_for_check:
        # Get name of field from properties.name.__uniqe_field
        name = schema['properties'][f].get('__uniqe_field', '')
        if not name:
            continue

        s = set()
        for x in data[f]:
            if x[name] in s:
                return (False, '"{}" should be unique in "{}"'.format(name, f))
            s.add(x[name])
    return (True, '')


def _validate(schema_name, data):
    schema = schema_dict[schema_name]

    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        return (False, e.message)

    return check_uniqe_filed_in_list(schema, data)


def _load_schema(filename):
    with open(filename, 'r') as f:
        schema = json.load(f)
    return schema


def create_schema_dict(filename_dict):
    ret = {}
    for name, fname in filename_dict.items():

        path = os.path.join(os.path.dirname(__file__), fname)

        ret[name] = _load_schema(path)
    return ret


schema_dict = create_schema_dict(_json_schema_files)


def json_validator(schema_name):
    def decorator_wrapper_jsonvalid(func):
        def wrapper(self, *args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                raise ApiExp.Structural
            if schema_name:
                json_validate(schema_name, data)

            return func(self, *args, data=data, **kwargs)
        return wrapper
    return decorator_wrapper_jsonvalid
