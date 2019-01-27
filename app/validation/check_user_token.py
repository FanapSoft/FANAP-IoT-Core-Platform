
from flask import request
from app.model import User
from app.exception import ApiExp
from app.authentication import verify_user_token

def check_user_token(func):
    def wrapper_usertoken(self, *args, **kargs):
        token = request.headers.get('userToken')

        user = verify_user_token(token)

        if not user:
            raise ApiExp.AccessDenied

        return func(self, *args, user=user, **kargs)

    return wrapper_usertoken
