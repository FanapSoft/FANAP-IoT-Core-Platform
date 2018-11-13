
from app.devicetype import get_by_devicetypeid_or_404
from app.model import Role
from app.exception import ApiExp
from app import db
from app.common import get_ok_response_body


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
    dt_attribute_list = [x['name'] for x in devicetype_attributes]

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
    q = Role.query.filter_by(owner=user)

    if 'name' in params:
        name_substr = params['name']
        q = q.filter(Role.name.contains(name_substr))
        print

    if 'deviceTypeId' in params:
        type_id = params['deviceTypeId']
        q = q.filter(Role.devicetype.has(typeid=type_id))

    # ToDo: Implement pagination for role_list

    role_list = [
        dict(
            id=x.roleid,
            name=x.name,
            deviceTypeName=x.devicetype.name,
            deviceTypeId=x.devicetype.typeid
        ) for x in q.all()
    ]

    return get_ok_response_body(
        data=dict(roles=role_list)
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

    # ToDo: Implement forceupdate after rolegrand for role_update

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

    db.session.delete(role)
    db.session.commit()

    return get_ok_response_body(
        data=dict(id=role.roleid)
    )
