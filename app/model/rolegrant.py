from app import db


class RoleGrant(db.Model):
    __tablename__ = 'rolegrant'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    granted_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def __repr__(self):
        return '<Grant User:{user} Role:{role} Device:{device}>'.format(
            user=self.granted_user.username,
            role=self.role.roleid,
            device=self.device.deviceid
        )
