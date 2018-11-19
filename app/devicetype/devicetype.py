from app.model import DeviceType
from app.exception import ApiExp
from app.common import get_ok_response_body, paginate
from app.common import contains_string_query
from app import db
from app.model import Role


def check_unique_name(user, devicetypename):
    dt = DeviceType.query.filter_by(
        name=devicetypename,
        owner=user
    ).first()

    if dt:
        raise ApiExp.DeviceTypeExists


def get_by_devicetypeid_or_404(user, devicetypeid):
    dt = DeviceType.query.filter_by(owner=user, typeid=devicetypeid).first()
    if not dt:
        raise ApiExp.DeviceTypeNotFound
    return dt


def convert_attribute_list_to_dict(attribute_list):
    return {x['name']: x['type'] for x in attribute_list}


def convert_dict_to_attribute_list(attibute_dict):
    return [dict(name=k, type=v) for k, v in attibute_dict.items()]


def devicetype_add(user, payload, params):
    name = payload['name']
    enc = payload['encryptionEnabled']
    description = payload.get('description', '')

    check_unique_name(user, name)

    dt = DeviceType(name=name, owner=user, enc=enc, description=description)

    dt.attributes = convert_attribute_list_to_dict(payload['attributeTypes'])

    new_devtype_id = dt.typeid

    db.session.add(dt)
    db.session.commit()

    return get_ok_response_body(data={"id": new_devtype_id})


def devicetype_list(user, params):
    q = DeviceType.query.filter_by(owner=user)

    q = contains_string_query(q, params, 'name', DeviceType.name)

    ret = paginate(q, params, dict(
        id=DeviceType.typeid,
        name=DeviceType.name
    ))

    devt_list = [dict(
        id=x.typeid,
        name=x.name
    ) for x in ret.items]

    return get_ok_response_body(
        data=dict(deviceTypes=devt_list),
        pageCnt=ret.pages
    )


def devicetype_show(user, devicetypeid, params):

    dt = get_by_devicetypeid_or_404(user, devicetypeid)

    return get_ok_response_body(
        name=dt.name,
        encrypted=dt.enc,
        id=dt.typeid,
        description=dt.description,
        attributeTypes=convert_dict_to_attribute_list(dt.attributes),
    )


def devicetype_delete(user, devicetypeid, params):

    dt = get_by_devicetypeid_or_404(user, devicetypeid)

    # Check if this devicetype is used by any device
    if dt.devices.count() != 0:
        raise ApiExp.DeviceInUse

    db.session.delete(dt)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=devicetypeid)
    )


def get_devicefields_metadata(devicetype):
    device_role = Role.query.filter_by(
        devicetype=devicetype, name='device').first()

    if not device_role:
        raise ApiExp.DeviceRoleNotDefined

    permissions = device_role.permissions

    data, metadata = [], []
    for f, p in permissions.items():
        if p == 'RW':
            data.append(f)
        else:
            metadata.append(f)

    return (data, metadata)
