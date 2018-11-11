from app import db
from .utils import unique_device_id, generate_enc_key


class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    deviceid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    devictype_id = db.Column(db.Integer, db.ForeignKey('devicetype.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    enc_key = db.Column(db.String(250))
    device_token = db.Column(db.String(250))
    serial_number = db.Column(db.String(128))
    label = db.Column(db.String(128))
    push_url = db.Column(db.String(128))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.deviceid:
            self.deviceid = unique_device_id()

        if not self.enc_key:
            self.enc_key = generate_enc_key()

        if not self.device_token:
            self.device_token = 'DTK'+generate_enc_key()

    def __repr__(self):
        return '<Device {name}-{id}'.format(
            name=self.name,
            id=self.deviceid,
        )
