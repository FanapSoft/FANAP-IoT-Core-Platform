# Store data by sending it to the URL
from app.model import Device
import time
from string import Template

from dataforward.pushurl import pushurl

class PushURLStorage:
    def __init__(self):
        pass

    def read_data(self, field_list, deviceid):
        # Read data is not supported. Only return empty dic
        return {}

    def store_data(self, data, deviceid):
        # First get device
        device = Device.query.filter_by(deviceid=deviceid).first()

        if not device:
            return False


        url = device.push_url
        if not url:
            # Push URL is not defined
            return 

        sub_str = dict(
            DEVICE_ID = deviceid,
            DEVICE_NAME = device.name,
            DEVICETYPE_ID = device.devicetype.typeid,
            DEVICETYPE_NAME = device.devicetype.name,
            TIMESTAMP = int(time.time())
        )

        if len(data) == 0:
            data =[{}]

        url_s = Template(url).safe_substitute(sub_str)
        pushurl.delay(url_s, data[0])
        
