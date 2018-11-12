from app.model import RoleGrant
from app.exception import ApiExp
from app.common import get_ok_response_body
from app import db
from app.user import get_by_username_or_404
from app.role import get_by_roleid_or_404
from app.device import get_by_deviceid_or_404


def check_unique_rolegrant(user, grant_user, role, device):
    rg = RoleGrant.query.filter_by(
        owner=user, granted_user=grant_user, role=role, device=device).first()
    if rg:
        raise ApiExp.RoleAlreadyGranted
    return rg


def role_grant(user, data, params):

    grant_user = get_by_username_or_404(data['username'])
    role = get_by_roleid_or_404(user, data['roleId'])
    device = get_by_deviceid_or_404(user, data['deviceId'])

    # Don't allow using device-role
    if role.name == 'device':
        raise ApiExp.RoleUpdateNotAllowed

    check_unique_rolegrant(user, grant_user, role, device)

    return dict(user=str(user), data=data, params=params, msg='role_grant')
