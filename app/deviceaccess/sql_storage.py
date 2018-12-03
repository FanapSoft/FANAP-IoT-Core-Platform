# Device Access and Storage (using ORM)
from app.model import DeviceData


class DataModelStorage:
    def __init__(self):
        pass

    def read_data(self, field_list, deviceid):
        return DeviceData.get_datadict(deviceid, field_list)

    def store_data(self, data, deviceid):
        if type(data) not in [list, tuple]:
            data = [data]

        for d in data:
            DeviceData.add_datadic(deviceid, d)
