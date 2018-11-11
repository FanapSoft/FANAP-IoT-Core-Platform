# Setup Application in Flask rest framework

from flask_restful import Resource
from flask import request

from app.validation import json_validator, check_user_token


class Role_Add(Resource):
    def post(self):
        return dict(msg='Role Add')


def connect(rest_api, endpoint):
    rest_api.add_resource(Role_Add, endpoint)
