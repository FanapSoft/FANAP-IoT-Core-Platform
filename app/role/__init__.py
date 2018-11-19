from .role_op import get_by_roleid_or_404
from .setup import connect
from .role_grant import role_get_device_permission_dict

__all__ = [
    'connect',
    'get_by_roleid_or_404',
    'role_get_device_permission_dict'
    ]
