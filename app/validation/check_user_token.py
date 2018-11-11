
from flask import request
from app.model import User
from app.exception import ApiExp


def check_user_token(func):
    def wrapper_usertoken(self, *args, **kargs):
        token = request.headers.get('userToken')

        username = User.verifyToken(token)

        if not username:
            raise ApiExp.AccessDenied

        return func(self, *args, user=username, **kargs)

    return wrapper_usertoken
