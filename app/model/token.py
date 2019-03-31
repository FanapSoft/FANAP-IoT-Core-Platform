from app import db
from sqlalchemy.orm import relationship

class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(250), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User")