# Check if user if owner of this deviceid or there is a role
# For accessing this device type for the user
#
#
# 1 D Check if user has access to the target device
# 2   Validate attributes based on the devicetype
# 3   Validate fields based on


from app.device import get_by_deviceid_or_404
from app.validation import devicedata_validator
from app.exception import ApiExp

import app.devicetype
from app.role import role_get_device_permission_dict
from app.common import get_ok_response_body
import app
import time
import json


def convert_attribute_list_to_dict(attribute_list):
    return {x['name']: x['value'] for x in attribute_list}


def validate_data_metadatafileds(fileds, user_data_dict):
    for fname in user_data_dict.keys():
        if fname not in fileds:
            raise ApiExp.Structural(
                dbg_msg='Can not send/write data for "{}"'.format(fname))


def check_user_write_field_access(user, device, user_field_list):
    pl = role_get_device_permission_dict(user, device)
    if not pl.check_write_access(user_field_list):
        raise ApiExp.AccessDenied(
            dbg_msg='No access for read/write device field')
    return True


def get_device_fields_with_read_permission(user, device):
    pl = role_get_device_permission_dict(user, device)
    return pl.get_fields_with_read_permission()


def create_msg_for_device(device, user_data):

    # ToDo: Find better location for preventing circular import
    from app.deviceaccess import enc_message

    if not isinstance(user_data, (list, tuple)):
        user_data = [user_data]

    dev_dict = dict(
        DeviceName=device.name,
        TimeStamp=int(time.time()),
        data=user_data
    )

    # ToDo: Perform encryption here!
    msg = json.dumps(dev_dict)

    if device.devicetype.enc:
        msg = enc_message(msg, device.enc_key)

    return msg


def write_send_common_validate(user, data, deviceid, params, is_write):
    # Check if any device is assigned to this user:
    device = get_by_deviceid_or_404(user, deviceid, look_in_granted=True)

    devicetype = device.devicetype

    user_data_dict = convert_attribute_list_to_dict(data['attributes'])

    # Validate user request body based on device-type
    devicedata_validator(devicetype.attributes, user_data_dict)

    data_fileds, metadata_fields = app.devicetype.get_devicefields_metadata(
        devicetype)

    # Validate if user is writing to meta-data and sending data to the metadata
    validate_data_metadatafileds(
        metadata_fields if is_write else data_fileds,
        user_data_dict)

    # Check if user (based on roles) has access to the requested fields
    check_user_write_field_access(user, device, user_data_dict.keys())

    dds = app.get_dds()

    if is_write:
        # Only store data in meta fields
        dds.store_data(user_data_dict, device.deviceid)
    else:
        # This is send-to-device operation
        # As mongo adds '_id' to the dict new copy required
        user_data_dict = convert_attribute_list_to_dict(data['attributes'])
        msg = create_msg_for_device(device, user_data_dict)
        dds.send_to_device(msg, device.deviceid)

    return get_ok_response_body(
        data={}
    )


def devicedata_write(user, data, deviceid, params):
    return write_send_common_validate(
        user, data, deviceid, params, is_write=True
    )


def devicedata_read(user, deviceid, params):
    # Check if any device is assigned to this user:
    device = get_by_deviceid_or_404(user, deviceid, look_in_granted=True)

    read_fields = get_device_fields_with_read_permission(user, device)

    dds = app.get_dds()
    x = dds.read_data(read_fields, device.deviceid)

    attributes = convert_field_dict_to_list(x)

    return get_ok_response_body(
        data=dict(attributes=attributes)
    )


def devicedata_send(user, data, deviceid, params):
    return write_send_common_validate(
        user, data, deviceid, params, is_write=False
    )


def convert_field_dict_to_list(field_dict):
    return [dict(name=f, value=v) for f, v in field_dict.items()]
