from app.model import Device
import app.devicetype
import jsonschema
from app.validation.devicedata_attribute import build_json_schema
from app.validation.jsoncheck import json_validate
from app.exception import ApiExp


def generate_devicedata_validator(devicetype):
    data_fileds, _ = app.devicetype.get_devicefields_metadata(
        devicetype)

    device_fields = {n: t for n,
                     t in devicetype.attributes.items() if n in data_fileds}

    return build_json_schema(device_fields)


def _validate_devicedata_object(validator, data):
    try:
        jsonschema.validate(data, validator)
    except jsonschema.ValidationError:
        return False
    return True


def validate_device_msg_list(deviceid, message_list):
    '''Check if received message from device is valid (based on devicetype)'''

    # First get device
    device = Device.query.filter_by(deviceid=deviceid).first()

    if not device:
        return False

    devicetype = device.devicetype

    validator = generate_devicedata_validator(devicetype)

    for data_object in message_list:
        if not _validate_devicedata_object(validator, data_object):
            return False
    return True


def validate_device_msg(deviceid, message):

    try:
        json_validate('data_from_device', message)
    except ApiExp.Structural:
        return False

    return validate_device_msg_list(deviceid, message['DATA'])
