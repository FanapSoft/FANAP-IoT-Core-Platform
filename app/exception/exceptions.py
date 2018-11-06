ErrorStatusCode = 500

MSG_DICT = {
    "MNC-M000" : "عملیات با موفقت انجام پذیرفت",
    "MNC-M001" : "خطای ساختاری",
    "MNC-M002" : "خطا در پارامتر‌های ارسالی، با پارامتر‌های صحیح تلاش کنید.",
    "MNC-M006" : "نوع دستگاه تکراری است",
    "MNC-M005" : "نوع دستگاه پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M007" : "نوع دستگاه در حال استفاده است",
    "MNC-M008" : "دستگاه پیدا نشد. دوباره تلاش کنید",
    "MNC-M009" : "دستگاه تکراری است",
    "MNC-M011" : "نقش پیدا نشد",
    "MNC-M012" : "این نقش برای نوع دستگاه قبلا ایجاد شده است",
    "MNC-M013" : "نقش روی دستگاه در حال استفاده است",
    "MNC-M014" : "کاربر پیدا نشد. لطفا دوباره تلاش کنید",
    "MNC-M119" : "نقش دستگاه تعریف نشده است",
    "MNC-M401" : "دسترسی غیر مجاز",
}

class ApiExp:

    class Structural(Exception):
        status_code = ErrorStatusCode
        msg_id = 'MNC-M001'

    class Parameters(Exception):
        status_code = ErrorStatusCode
        msg_id = 'MNC-M002'
    
    class Khafan(Exception):
        status_code = 411
        msg_id = 'MNC-M012'

        def __init__(self, values={}):
            self.payload = values




def get_message(msg_id):
    return MSG_DICT.get(msg_id, 'Unknown')