from app.validation import json_validate
from app.model import DeviceType
from app.exception import ApiExp, get_ok_message_dict
from app import db
import time


def check_unique_name(username, devicetypename):
    dt = DeviceType.query.filter(
        DeviceType.name == devicetypename, 
        DeviceType.username == username
    ).first()

    if dt:
        raise ApiExp.DeviceTypeExists



def devicetype_add(user, payload, params):
    json_validate('devicetype', payload)

    name = payload['name']
    enc = payload['encryptionEnabled']
    description = payload.get('description', '')

    check_unique_name(user, name)

    dt = DeviceType(name=name, username = user, enc=enc, description=description)

    dt.attributes = payload['attributeTypes']

    new_devtype_id = dt.typeid

    db.session.add(dt)
    db.session.commit()

    return dict(
        timestamp=time.time(),  
        message = get_ok_message_dict(), 
        data = {"id":new_devtype_id},
        )

def devicetype_list(user, params):


    pass