import jsonschema
from app.exception import ApiExp


def _conv_plat_type_to_json_type(type_object):
    td = dict(String='string', Number='number', Boolean='boolean')

    if type(type_object) in [list, tuple]:
        return dict(type='string', enum=type_object)
    else:
        return dict(type=td[type_object])


def build_json_schema(devicetype_dict):
    return dict(
        properties={
            n: _conv_plat_type_to_json_type(v)
            for n, v in devicetype_dict.items()
        },
        additionalProperties=False,
    )


def _validator(devicetype_dict, attribute_dict):
    schema = build_json_schema(devicetype_dict)

    try:
        jsonschema.validate(attribute_dict, schema)
    except jsonschema.ValidationError as e:
        return (False, e.message)

    return (True, '')


def devicedata_validator(devicetype_dict, attribute_dict):
    payload_ok, payload_chk_msg = _validator(devicetype_dict, attribute_dict)

    if not payload_ok:
        raise ApiExp.Structural(dbg_msg=payload_chk_msg)
    return True
