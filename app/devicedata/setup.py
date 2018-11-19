from flask_restful import Resource
from flask import request
from app.validation import json_validator, check_user_token

from .devicedata_op import devicedata_write, devicedata_read


class DevieData_Write_Read(Resource):
    @json_validator('devicedata_write')
    @check_user_token
    def post(self, user, deviceid, data):
        return devicedata_write(user, data, deviceid, request.args)

    @check_user_token
    def get(self, deviceid, user):
        return devicedata_read(user, deviceid, request.args)


def connect(rest_api, endpoint):
    rest_api.add_resource(DevieData_Write_Read, endpoint+'/<deviceid>')
