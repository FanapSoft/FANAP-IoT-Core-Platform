ErrorStatusCode = 500

MSG_DICT = {
    "MNC-M000": "Success!",
    "MNC-M001": "Syntax Error",
    "MNC-M002": "Parameter Error",
    "MNC-M003": "Number Exceeded Error",
    "MNC-M006": "DeviceType already Exists",
    "MNC-M005": "DeviceType Not Found",
    "MNC-M007": "DeviceType is In Use",
    "MNC-M008": "Device Not Found",
    "MNC-M009": "Device Already Exists",
    "MNC-M011": "Role Not Found",
    "MNC-M012": "RoleName for DeviceType already Exists",
    "MNC-M013": "Role is In Use",
    "MNC-M014": "User Not Found",
    "MNC-M015": "Role for Device not Found",
    "MNC-M017": "Role is not granted to user",
    "MNC-M119": "Device Role Not Defined",
    "MNC-M120": "Username already Exists",
    "MNC-M121": "Device Role can't Change or Granted",
    "MNC-M122": "Role has already Granted to Users",
    "MNC-M401": "Access Denied",
}


class ApiExp:

    class Structural(Exception):
        # status_code = ErrorStatusCode
        msg_id = 'MNC-M001'

        def __init__(self, **args):
            self.payload = args

    class Parameters(Exception):
        msg_id = 'MNC-M002'

        def __init__(self, **args):
            self.payload = args

    class PageNumExceed(Exception):
        msg_id = 'MNC-M003'

    class UserExists(Exception):
        msg_id = 'MNC-M120'

    class AccessDenied(Exception):
        msg_id = 'MNC-M401'

        def __init__(self, **args):
            self.payload = args

    class DeviceTypeExists(Exception):
        msg_id = 'MNC-M006'

    class DeviceTypeNotFound(Exception):
        msg_id = 'MNC-M005'

    class DeviceInUse(Exception):
        msg_id = 'MNC-M007'

    class DeviceExists(Exception):
        msg_id = 'MNC-M009'

    class DeviceNotFound(Exception):
        msg_id = 'MNC-M008'

    class RoleNotFound(Exception):
        msg_id = 'MNC-M011'

    class RoleExists(Exception):
        msg_id = 'MNC-M012'

    class RoleForDeviceNotFound(Exception):
        msg_id = 'MNC-M015'

    class RoleUpdateNotAllowed(Exception):
        msg_id = 'MNC-M121'

    class DeviceRoleNotDefined(Exception):
        msg_id = 'MNC-M119'

    class UserNotFound(Exception):
        msg_id = 'MNC-M014'

    class RoleAlreadyGranted(Exception):
        msg_id = 'MNC-M122'

    class RoleNotGranted(Exception):
        msg_id = 'MNC-M017'


def get_message(msg_id):
    return MSG_DICT.get(msg_id, 'Unknown')
