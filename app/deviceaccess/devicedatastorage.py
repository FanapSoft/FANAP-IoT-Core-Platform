# Device Access and Storage controll

from app.devicedata import validate_decode_device_msg


class DeviceDataStorage:

    def __init__(self, storage, device_data_push=None):
        self.sender = None
        if not isinstance(storage, (list, tuple)):
            storage = [storage]
        self.storage = storage
        self.data_push = device_data_push

    def get_device_message(self, msg, deviceid):

        # msg is json data in string format
        msg_data = validate_decode_device_msg(deviceid, msg)
        if not msg_data:
            # 'ToDo: Generate log for message with access issue'
            return False

        if self.data_push:
            self.data_push.store_data(msg_data, deviceid)

        self._store(msg_data, deviceid)

    def send_to_device(self, msg, deviceid):
        if self.sender:
            self.sender(msg, deviceid)

    def read_data(self, field_list, deviceid):
        ret = {}

        for s in self.storage:
            ret.update( 
                s.read_data(
                    field_list,
                    deviceid
                )
            )

        return ret

    def store_data(self, data, deviceid):
        self._store(data, deviceid)

    def set_device_sender(self, sender):
        self.sender = sender

    def _store(self, data, deviceid):
        for s in self.storage:
            s.store_data(data, deviceid)