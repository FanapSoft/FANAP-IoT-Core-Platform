ErrorStatusCode = 500

MSG_DICT = {
    "MNC-M000": "عملیات با موفقت انجام پذیرفت",
    "MNC-M001": "خطای ساختاری",
    "MNC-M002": "خطا در پارامتر‌های ارسالی، با پارامتر‌های صحیح تلاش کنید.",
    "MNC-M006": "نوع دستگاه تکراری است",
    "MNC-M005": "نوع دستگاه پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M007": "نوع دستگاه در حال استفاده است",
    "MNC-M008": "دستگاه پیدا نشد. دوباره تلاش کنید",
    "MNC-M009": "دستگاه تکراری است",
    "MNC-M011": "نقش پیدا نشد",
    "MNC-M012": "این نقش برای نوع دستگاه قبلا ایجاد شده است",
    "MNC-M013": "نقش روی دستگاه در حال استفاده است",
    "MNC-M014": "کاربر پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M119": "نقش دستگاه تعریف نشده است",
    "MNC-M120": "اسم کاربر تکراری است",
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

    class UserExists(Exception):
        msg_id = 'MNC-M120'

    class AccessDenied(Exception):
        msg_id = 'MNC-M401'

    class DeviceTypeExists(Exception):
        msg_id = 'MNC-M006'

    class DeviceTypeNotFound(Exception):
        msg_id = 'MNC-M005'

    class DeviceExists(Exception):
        msg_id = 'MNC-M009'

    class DeviceNotFound(Exception):
        msg_id = 'MNC-M008'

    class RoleExists(Exception):
        msg_id = 'MNC-M012'


def get_message(msg_id):
    return MSG_DICT.get(msg_id, 'Unknown')
