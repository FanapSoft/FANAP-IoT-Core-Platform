from app import db
from .utils import unique_user_token
from sqlalchemy import exc


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    user_id = db.Column(db.Integer)
    given_name = db.Column(db.String(250), unique=True, nullable=False)
    family_name = db.Column(db.String(250), unique=True, nullable=False)

    devicetypes = db.relationship('DeviceType', backref='owner')
    devices = db.relationship('Device', backref='owner')
    roles = db.relationship('Role', backref='owner', lazy='dynamic')
    owned_rolegrants = db.relationship(
        'RoleGrant', backref='owner',
        lazy='dynamic', foreign_keys='RoleGrant.owner_id')
    grantedroles = db.relationship(
        'RoleGrant', backref='granted_user',
        lazy='dynamic', foreign_keys='RoleGrant.granted_user_id')

    def __repr__(self):
        return '<{username} {user_id}>'.format(
            username=self.username,
            user_id=self.user_id
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
