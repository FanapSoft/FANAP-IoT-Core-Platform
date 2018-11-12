# Setup Application in Flask rest framework

from flask_restful import Resource
from flask import request

from app.validation import json_validator, check_user_token
from .role_op import role_add, role_list


class Role_Add_List(Resource):
    @json_validator('role_add')
    @check_user_token
    def post(self, user, data):
        return role_add(user, data, request.args)

    @check_user_token
    def get(self, user):
        return role_list(user, request.args)


def connect(rest_api, endpoint):
    rest_api.add_resource(Role_Add_List, endpoint)
