# Setup Application in Flask rest framework

from flask_restful import Resource
from app.validation import json_validator
from .podtoken import userlogin, callback

from flask import request

class GetToken(Resource):
    def get(self):
        return userlogin()

class CallBack(Resource):
    def get(self):
        return callback(request.args)

def connect(rest_api, endpoint):
    rest_api.add_resource(GetToken, endpoint + '/token')
    rest_api.add_resource(CallBack, endpoint + '/callback')