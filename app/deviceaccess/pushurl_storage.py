# Store data by sending it to the URL
from app.model import DeviceData


class PushURLStorage:
    def __init__(self):
        pass

    def read_data(self, field_list, deviceid):
        # Read data is not supported. Only return empty dic
        return {}

    def store_data(self, data, deviceid):
        # ToDo: Complete storing DATA by sending to the URL
        print(">>>>> Storage is called for data={} deviceid={}".format(data,deviceid))
