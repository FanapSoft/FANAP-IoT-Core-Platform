from app.devicetype import get_by_devicetypeid_or_404
from app.exception import ApiExp
from app.model import Device
from app.model import RoleGrant
from app import db
from app.common import get_ok_response_body, paginate
from app.common import contains_string_query
from sqlalchemy import or_


def check_unique_name(user, device_name):
    dt = Device.query.filter_by(
        name=device_name,
        owner=user
    ).first()

    if dt:
        raise ApiExp.DeviceExists


def get_by_deviceid_or_404(user, deviceid, look_in_granted=False):
    dev = Device.query.filter_by(owner=user, deviceid=deviceid).first()

    if dev:
        return dev
    elif not look_in_granted:
        raise ApiExp.DeviceNotFound

    rg = RoleGrant.query.filter(RoleGrant.granted_user == user).filter(
        RoleGrant.device.has(deviceid=deviceid)).first()

    if not rg:
        raise ApiExp.DeviceNotFound

    return rg.device


def device_add(user, payload, params):
    devicetype_id = payload['deviceTypeId']
    name = payload['name']

    devicetype = get_by_devicetypeid_or_404(user, devicetype_id)

    check_unique_name(user, name)

    # Make sure device-role is defined
    if not devicetype.roles.filter_by(name='device').first():
        raise ApiExp.DeviceRoleNotDefined

    # ToDo: Implement attributeValues for setting initial of meta-data

    new_device = Device(
        name=name,
        serial_number=payload.get('serialNumber', ''),
        label=payload.get('label', ''),
        push_url=payload.get('pushURL', ''),
        owner=user,
        devicetype=devicetype
    )

    db.session.add(new_device)
    db.session.commit()

    return get_ok_response_body(
        data=dict(
            id=new_device.deviceid,
            encryptionKey=new_device.enc_key,
            deviceToken=new_device.device_token,
        )
    )


def device_list(user, params):

    condition = [(Device.owner == user),
                 (Device.grantroles.any(RoleGrant.granted_user == user))]

    if 'isOwned' in params:
        if params['isOwned']:
            condition = [(Device.owner == user)]
        else:
            condition = [(Device.grantroles.any(
                RoleGrant.granted_user == user))]

    q = Device.query.filter(or_(*condition))

    q = contains_string_query(q, params, 'name', Device.name)

    ret = paginate(q, params, dict(
        id=Device.deviceid,
        name=Device.name
    ))

    dev_list = [
        dict(
            id=x.deviceid,
            name=x.name,
            isOwned=(user == x.owner)
        ) for x in ret.items
    ]

    return get_ok_response_body(
        data=dict(devices=dev_list),
        pageCnt=ret.pages,
    )


def device_show(user, deviceid, params):
    device = get_by_deviceid_or_404(user, deviceid)

    ret_data = dict(
        id=device.deviceid,
        name=device.name,
        deviceTypeId=device.devicetype.typeid,
        deviceTypeName=device.devicetype.name,
        serialNumber=device.serial_number,
        encryptionKey=device.enc_key,
        deviceToken=device.device_token,
        pushURL=device.push_url
    )

    return get_ok_response_body(
        data=ret_data
    )


def device_edit(user, data, deviceid, params):
    device = get_by_deviceid_or_404(user, deviceid)

    # If new name is provided check for a device with same name
    if 'name' in data:
        new_name = data['name']
        if new_name != device.name:
            check_unique_name(user, new_name)
            device.name = new_name

    if 'serialNumber' in data:
        device.serial_number = data['serialNumber']

    if 'pushURL' in data:
        device.push_url = data['pushURL']

    db.session.commit()

    return get_ok_response_body(
        data=dict(id=device.deviceid)
    )


def device_delete(user, deviceid):
    device = get_by_deviceid_or_404(user, deviceid)

    db.session.delete(device)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=deviceid)
    )
