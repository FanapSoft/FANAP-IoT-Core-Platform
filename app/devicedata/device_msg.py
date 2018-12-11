from app.model import Device
import app.devicetype
import jsonschema
from app.validation.devicedata_attribute import build_json_schema
from app.validation.jsoncheck import json_validate
from app.exception import ApiExp
import json


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


def dec_device_msg(deviceid, message):
    '''Check if received message should be decrypted'''

    from app.deviceaccess import dec_message

    # First get device
    device = Device.query.filter_by(deviceid=deviceid).first()

    if not device:
        return False

    if not device.devicetype.enc:
        return message

    return dec_message(message, device.enc_key)


def validate_decode_device_msg(deviceid, message):

    message = dec_device_msg(deviceid, message)

    if not message:
        return False

    # Here convert message from json
    try:
        if not isinstance(message, str):
            message = message.decode('utf-8')
        msg_data = json.loads(message)
    except json.decoder.JSONDecodeError:
        # ToDo: Log missed packets here
        return False

    try:
        json_validate('data_from_device', msg_data)
    except ApiExp.Structural:
        return False

    if not validate_device_msg_list(deviceid, msg_data['data']):
        return False

    return msg_data['data']
