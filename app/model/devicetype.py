from app import db
import json
from .utils import unique_devicetype_token


class DeviceType(db.Model):
    __tablename__ = 'devicetype'
    id = db.Column(db.Integer, primary_key=True)
    typeid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    enc = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    _attributes = db.Column(db.Text)
    devices = db.relationship('Device', backref='devicetype', lazy='dynamic')
    roles = db.relationship('Role', backref='devicetype', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.typeid:
            self.typeid = unique_devicetype_token()

        self.attributes = []

    @property
    def attributes(self):
        return json.loads(self._attributes)

    @attributes.setter
    def attributes(self, value):
        self._attributes = json.dumps(value)

    def __repr__(self):
        return '<DeviceType {name}-{id}>'.format(
            name=self.name,
            id=self.typeid
        )

    def get_devicerole(self):
        return self.roles.query.filter_by(name='device').first()
