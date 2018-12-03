from app import db
from sqlalchemy import exc
import json

# Data model for storing device-data in relational database.
# Each data field stored in a separate row.


class DeviceData(db.Model):
    __tablename__ = 'devicedata'
    id = db.Column(db.Integer, primary_key=True)
    deviceid = db.Column(db.String(20), nullable=False)
    field = db.Column(db.String, nullable=False)
    _data = db.Column(db.String)

    def __repr__(self):
        return '<{deviceid} {field}={data}>'.format(
            deviceid=self.deviceid,
            field=self.field,
            data=self.data
        )

    @property
    def data(self):
        return json.loads(self._data)

    @data.setter
    def data(self, value):
        self._data = json.dumps(value)

    @staticmethod
    def add_datadic(deviceid, data_dic):
        ret = {}
        if data_dic:
            for field, value in data_dic.items():
                d = DeviceData(
                    deviceid=deviceid,
                    field=field,
                )
                d.data = value

                db.session.add(d)
                ret[field] = d

            try:
                db.session.commit()
                return ret
            except exc.IntegrityError as e:
                print(e)
                db.session.rollback()
                return False

    @staticmethod
    def get_field_data(deviceid, field):
        dd = DeviceData.query.filter_by(
            field=field,
            deviceid=deviceid,
        ).order_by(
            DeviceData.id.desc()
        ).first()

        if not dd:
            return None
        else:
            return dd.data

    @staticmethod
    def get_datadict(deviceid, field_list):
        return {
            name: DeviceData.get_field_data(deviceid, name)
            for name in field_list
        }
