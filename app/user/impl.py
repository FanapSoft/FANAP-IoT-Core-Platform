# Implementation for user Add/List

from app.exception import ApiExp
from app.model import User
import time


def user_list():
    
    user_list = [dict(name=usr.username, token=usr.token) 
        for usr in User.query.all()]

    return dict(timestamp=time.time(), users=user_list)



def user_add(data):
    username = data['name']
    token = User.add(username)

    if not token:
        raise ApiExp.UserExists

    return dict(message='User created', name=username, token=token) 





