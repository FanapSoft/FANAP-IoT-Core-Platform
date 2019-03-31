# Setup Application in Flask rest framework

from flask_restful import Resource
from app.validation import json_validator, check_user_token
from .podtoken import userlogin, callback
from .software import software_delete, software_register

from flask import request

class GetToken(Resource):
    def get(self):
        return userlogin()

class CallBack(Resource):
    def get(self):
        return callback(request.args)

class SoftwareUser(Resource):
    @check_user_token
    def put(self, user):
        return software_register(user, request.args)

    @check_user_token
    def delete(self, user):
        return software_delete(user, request.args)

def connect(rest_api, endpoint):
    rest_api.add_resource(GetToken, endpoint + '/token')
    rest_api.add_resource(CallBack, endpoint + '/callback')
    rest_api.add_resource(SoftwareUser, endpoint + '/software')
