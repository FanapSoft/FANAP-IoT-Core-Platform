# Implementation for user Add/List

from app.exception import ApiExp
from app.model import User
import time

def get_by_username_or_404(username):
    usr = User.query.filter_by(username=username).first()
    if not usr:
        raise ApiExp.UserNotFound
    return usr
