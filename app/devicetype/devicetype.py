from app.model import DeviceType
from app.exception import ApiExp
from app.common import get_ok_response_body
from app import db


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


def devicetype_add(user, payload, params):
    name = payload['name']
    enc = payload['encryptionEnabled']
    description = payload.get('description', '')

    check_unique_name(user, name)

    dt = DeviceType(name=name, owner=user, enc=enc, description=description)

    dt.attributes = payload['attributeTypes']

    new_devtype_id = dt.typeid

    db.session.add(dt)
    db.session.commit()

    return get_ok_response_body(data={"id": new_devtype_id})


def devicetype_list(user, params):
    q = DeviceType.query.filter_by(owner=user)

    if 'name' in params:
        name_substr = params['name']
        q = q.filter(DeviceType.name.contains(name_substr))

    # ToDo: Implement pagination

    devt_list = [dict(
        id=x.typeid,
        name=x.name
    ) for x in q.all()]

    return get_ok_response_body(
        data=dict(deviceTypes=devt_list)
    )


def devicetype_show(user, devicetypeid, params):

    dt = get_by_devicetypeid_or_404(user, devicetypeid)

    return get_ok_response_body(
        name=dt.name,
        encrypted=dt.enc,
        id=dt.typeid,
        description=dt.description,
        attributeTypes=dt.attributes,
    )


def devicetype_delete(user, devicetypeid, params):

    dt = get_by_devicetypeid_or_404(user, devicetypeid)

    # ToDo: Check if any device is defined for given devicetype
    db.session.delete(dt)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=devicetypeid)
    )
