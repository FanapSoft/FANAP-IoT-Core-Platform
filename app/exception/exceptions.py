ErrorStatusCode = 500

MSG_DICT = {
    "MNC-M000": "عملیات با موفقت انجام پذیرفت",
    "MNC-M001": "خطای ساختاری",
    "MNC-M002": "خطا در پارامتر‌های ارسالی، با پارامتر‌های صحیح تلاش کنید.",
    "MNC-M003": "شماره شروع لیست بیش از تعداد کل آیتم های لیست است.",
    "MNC-M006": "نوع دستگاه تکراری است",
    "MNC-M005": "نوع دستگاه پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M007": "نوع دستگاه در حال استفاده است",
    "MNC-M008": "دستگاه پیدا نشد. دوباره تلاش کنید",
    "MNC-M009": "دستگاه تکراری است",
    "MNC-M011": "نقش پیدا نشد",
    "MNC-M012": "این نقش برای نوع دستگاه قبلا ایجاد شده است",
    "MNC-M013": "نقش روی دستگاه در حال استفاده است",
    "MNC-M014": "کاربر پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M015": "نقش برای دستگاه پیدا نشد.",
    "MNC-M017": "نقش مورد نظر به کاربر اعطا نشده است. لطفا دوباره تلاش کنید",
    "MNC-M119": "نقش دستگاه تعریف نشده است",
    "MNC-M120": "اسم کاربر تکراری است",
    "MNC-M121": "نقش دستگاه قابل تغییر و اعطا نیست",
    "MNC-M122": "نقش اعطا شده است",
    "MNC-M401": "دسترسی غیر مجاز",
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
