from app.model import RoleGrant
from app.exception import ApiExp
from app.common import get_ok_response_body, field_equal_query
from app import db
from app.user import get_by_username_or_404
from app.role import get_by_roleid_or_404
from app.device import get_by_deviceid_or_404


def get_rolegrant(user, grant_user, role, device):
    rg = RoleGrant.query.filter_by(
        owner=user, granted_user=grant_user, role=role, device=device).first()
    return rg


def check_unique_rolegrant(user, grant_user, role, device):
    rg = get_rolegrant(user, grant_user, role, device)

    if rg:
        raise ApiExp.RoleAlreadyGranted


def get_rolegrant_or_404(user, grant_user, role, device):
    rg = get_rolegrant(user, grant_user, role, device)

    if not rg:
        raise ApiExp.RoleNotGranted
    return rg


def check_role_defined_for_devicetype(role, device):
    if role.devicetype != device.devicetype:
        raise ApiExp.RoleForDeviceNotFound
    return True


def role_grant(user, data, params):

    grant_user = get_by_username_or_404(data['username'])
    role = get_by_roleid_or_404(user, data['roleId'])
    device = get_by_deviceid_or_404(user, data['deviceId'])

    # Don't allow using device-role
    if role.name == 'device':
        raise ApiExp.RoleUpdateNotAllowed

    check_unique_rolegrant(user, grant_user, role, device)

    # Check if role is defined for decicetype
    check_role_defined_for_devicetype(role, device)

    rg = RoleGrant(owner=user, granted_user=grant_user,
                   role=role, device=device)

    db.session.add(rg)
    db.session.commit()

    return get_ok_response_body()


def role_grant_list(user, params):

    q = RoleGrant.query.filter_by(owner=user)

    q = field_equal_query(q, params, 'deviceId',
                          RoleGrant.device, 'deviceid')

    q = field_equal_query(q, params, 'username',
                          RoleGrant.granted_user, 'username')

    q = field_equal_query(q, params, 'roleId',
                          RoleGrant.role, 'roleid')

    # ToDo: Implement pagination for rolegrant_list plus sortby

    rolegrants = [
        dict(
            deviceTypeName=rg.device.devicetype.name,
            deviceTypeId=rg.device.devicetype.typeid,
            deviceName=rg.device.name,
            deviceId=rg.device.deviceid,
            roleName=rg.role.name,
            roleId=rg.role.roleid,
            username=rg.granted_user.username,
            userid=rg.granted_user.username,
        ) for rg in q.all()
    ]

    return get_ok_response_body(
        data=dict(
            roles=rolegrants
        )
    )


def role_take(user, data, params):
    grant_user = get_by_username_or_404(data['username'])
    role = get_by_roleid_or_404(user, data['roleId'])
    device = get_by_deviceid_or_404(user, data['deviceId'])

    # Don't allow using device-role
    if role.name == 'device':
        raise ApiExp.RoleUpdateNotAllowed

    rg = get_rolegrant_or_404(user, grant_user, role, device)

    db.session.delete(rg)
    db.session.commit()

    return get_ok_response_body()
