
from app.devicetype import get_by_devicetypeid_or_404
from app.exception import ApiExp
from app import db
from app.model import Role, DeviceType
from app.common import get_ok_response_body, paginate
from app.common import contains_string_query, field_equal_query


def check_unique_role_name(user, role_name, devicetype):
    role = Role.query.filter_by(
        name=role_name,
        owner=user,
        devicetype=devicetype
    ).first()

    if role:
        raise ApiExp.RoleExists


def get_by_roleid_or_404(user, roleid):
    role = Role.query.filter_by(owner=user, roleid=roleid).first()
    if not role:
        raise ApiExp.RoleNotFound
    return role


def generate_role_dict(
        devicetype,
        add_permission_list,
        is_device_role=False):

    devicetype_attributes = devicetype.attributes

    # Generate attribute list
    dt_attribute_list = list(devicetype_attributes.keys())

    # For device role inclue all fields with default value
    if is_device_role:
        res = dict.fromkeys(dt_attribute_list, 'N')
    else:
        res = {}

    for field in add_permission_list:
        name, permission = field['attributeTypeName'], field['permission']

        if name not in dt_attribute_list:
            raise ApiExp.Parameters

        if is_device_role and permission not in ['N', 'RW']:
            raise ApiExp.Parameters

        res[name] = permission

    return res


def generate_role_response_list(role):
    return [
        dict(
            attributeTypeName=n,
            permission=v
        ) for n, v in
        role.permissions.items()
    ]


def role_add(user, data, params):

    devicetype = get_by_devicetypeid_or_404(user, data['deviceTypeId'])

    name = data['name']

    check_unique_role_name(user, name, devicetype)

    is_device_role = (name == 'device')

    per_dict = generate_role_dict(
        devicetype, data['attributePermissions'], is_device_role)

    new_role = Role(
        name=name,
        owner=user,
        devicetype=devicetype,
        description=data.get('description', '')
    )

    new_role.permissions = per_dict

    new_role_id = new_role.roleid

    db.session.add(new_role)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=new_role_id)
    )


def role_list(user, params):
    q = Role.query.join(Role.devicetype).filter_by(owner=user)

    q = contains_string_query(q, params, 'name', Role.name)

    q = field_equal_query(q, params, 'deviceTypeId',
                          Role.devicetype, 'typeid')

    ret = paginate(q, params, dict(
        id=Role.roleid,
        name=Role.name,
        deviceTypeName=DeviceType.name,
        deviceTypeId=DeviceType.typeid
    ))

    role_list = [
        dict(
            id=x.roleid,
            name=x.name,
            deviceTypeName=x.devicetype.name,
            deviceTypeId=x.devicetype.typeid
        ) for x in ret.items
    ]

    return get_ok_response_body(
        data=dict(roles=role_list),
        pageCnt=ret.pages
    )


def role_show(user, roleid, params):
    role = get_by_roleid_or_404(user, roleid)

    per_list = generate_role_response_list(role)

    return get_ok_response_body(
        data=dict(
            name=role.name,
            description=role.description,
            deviceTypeId=role.devicetype.typeid,
            attributePermissions=per_list
        )
    )


def role_update(user, data, roleid, params):
    role = get_by_roleid_or_404(user, roleid)

    # ToDo: Implement forceupdate after rolegrant for role_update
    # ToDo: Accept update for device-role

    if role.name == 'device' or data.get('name', '') == 'device':
        # Dont allow chaning device-role
        raise ApiExp.RoleUpdateNotAllowed

    if 'attributePermissions' in data:
        devicetype = role.devicetype
        per_dict = generate_role_dict(
            devicetype,
            data['attributePermissions'],
            False)

        role.permissions = per_dict

    if 'description' in data:
        role.description = data['description']

    if 'name' in data:
        new_name = data['name']
        if new_name != role.name:
            check_unique_role_name(user, new_name, role.devicetype)
            role.name = new_name

    db.session.commit()

    return get_ok_response_body(
        data=dict(id=role.roleid)
    )


def role_delete(user, roleid, params):
    role = get_by_roleid_or_404(user, roleid)

    # ToDo: Implement "forceDelete" after rolegrant for role-delete

    if role.name == 'device':
        # Dont allow deleting device role
        raise ApiExp.RoleUpdateNotAllowed

    db.session.delete(role)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=role.roleid)
    )
