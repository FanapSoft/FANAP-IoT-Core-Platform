from app import db
import json
from .utils import unique_role_id


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    roleid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    devictype_id = db.Column(db.Integer, db.ForeignKey('devicetype.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    _permissions = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.roleid:
            self.roleid = unique_role_id()

        self.permissions = []

    @property
    def permissions(self):
        return json.loads(self._permissions)

    @permissions.setter
    def permissions(self, value):
        self._permissions = json.dumps(value)

    def __repr__(self):
        return '<Role {name}-{id}>'.format(
            name=self.name,
            id=self.roleid
        )
