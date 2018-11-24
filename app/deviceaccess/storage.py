# Device Access and Storage controll

from app.devicedata import validate_decode_device_msg
from pymongo import MongoClient


class DeviceDataStorage:
    DB_NAME = 'device_data'

    def __init__(self, application):
        db_client = MongoClient(application.config['DATASTORAGE_URI'])
        self.db = db_client[DeviceDataStorage.DB_NAME]
        self.sender = None

    def get_device_message(self, msg, deviceid):

        # msg is json data in string format
        msg_data = validate_decode_device_msg(deviceid, msg)
        if not msg_data:
            # 'ToDo: Generate log for message with access issue'
            return False
        self.store_data(msg_data, deviceid)

    def send_to_device(self, msg, deviceid):
        if self.sender:
            self.sender(msg, deviceid)

    def store_data(self, data, deviceid):
        if type(data) not in [list, tuple]:
            data = [data]

        # Get device collection
        collection = self.db[deviceid]

        collection.insert_many(data)

    def read_data(self, field_list, deviceid):
        ret = {}
        for field in field_list:
            q = self.query_last_field(field, deviceid)
            if not q:
                ret[field] = None
            else:
                ret[field] = q[0][field]
        return ret

    def query_last_field(self, field_name, deviceid):

        c = self.db[deviceid]

        return list(
            c.find({field_name: {"$exists": True}}).hint(
                [('$natural', -1)]).limit(1)
        )

    def set_device_sender(self, sender):
        self.sender = sender
