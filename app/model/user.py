from app import db
from .utils import unique_user_token 

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), unique = True, nullable=False )
    token = db.Column(db.String(20), unique = True )
    devicetypes = db.relationship('DeviceType', backref='owner')

    def __repr__(self):
        return '<{username} {token}>'.format(username = self.username, token = self.token)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.token:
            self.token = unique_user_token()


    @staticmethod
    def add(username):
        username = username.strip()
        
        user = User(username = username)

        db.session.add(user)

        try:
            db.session.commit()
            return user.token
        except :
            db.session.rollback()
            return False

    
    @staticmethod
    def verifyToken(token):
        if not token:
            return None
            
        usr = User.query.filter(User.token == token).first()

        if usr:
            return usr
        else:
            return None