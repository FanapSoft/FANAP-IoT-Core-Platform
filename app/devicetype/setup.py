# Setup Application in Flask rest framework

from flask_restful import Resource
from flask import request

from app.validation import check_jsonbody, check_user_token

from .devicetype import *


class DeviceType_List_Add(Resource):

    @check_jsonbody
    @check_user_token
    def post(self, user, data):
        return devicetype_add(user, data, request.args)

    @check_user_token
    def get(self, user):
        return devicetype_list(user, request.args)


class DeviceType_Show(Resource):

    @check_user_token
    def get(self, devicetypeid, user):
        return devicetype_show(user, devicetypeid, request.args)

    @check_user_token
    def delete(self, user, devicetypeid):
        return devicetype_delete(user, devicetypeid, request.args)


def connect(rest_api, endpoint):
    rest_api.add_resource(DeviceType_List_Add, endpoint)
    rest_api.add_resource(DeviceType_Show, endpoint+ '/<devicetypeid>')
    