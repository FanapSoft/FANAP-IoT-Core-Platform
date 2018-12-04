# Device Access and Storage controll

from app.devicedata import validate_decode_device_msg


class DeviceDataStorage:

    def __init__(self, storage):
        self.sender = None
        self.storage = storage

    def get_device_message(self, msg, deviceid):

        # msg is json data in string format
        msg_data = validate_decode_device_msg(deviceid, msg)
        if not msg_data:
            # 'ToDo: Generate log for message with access issue'
            return False
        self.storage.store_data(msg_data, deviceid)

    def send_to_device(self, msg, deviceid):
        if self.sender:
            self.sender(msg, deviceid)

    def read_data(self, field_list, deviceid):
        return self.storage.read_data(
            field_list,
            deviceid
        )

    def store_data(self, data, deviceid):
        self.storage.store_data(data, deviceid)

    def set_device_sender(self, sender):
        self.sender = sender
