from flask_restful import Resource
from flask import request
from app.validation import json_validator, check_user_token
from .device import device_add, device_list
from .device import device_show, device_edit, device_delete


class Device_Add_List(Resource):

    @json_validator('device')
    @check_user_token
    def post(self, user, data):
        return device_add(user, data, request.args)

    @check_user_token
    def get(self, user):
        return device_list(user, request.args)


class Device_Show_Edit_Delete(Resource):
    @check_user_token
    def get(self, deviceid, user):
        return device_show(user, deviceid, request.args)

    @json_validator('device_edit')
    @check_user_token
    def put(self, user, deviceid, data):
        return device_edit(user, data, deviceid, request.args)

    @check_user_token
    def delete(self, user, deviceid):
        return device_delete(user, deviceid)


def connect(rest_api, endpoint):
    rest_api.add_resource(Device_Add_List, endpoint)
    rest_api.add_resource(Device_Show_Edit_Delete, endpoint + '/<deviceid>')
