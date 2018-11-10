# Setup Application in Flask rest framework

from flask_restful import Resource
from flask import request

from app.validation import check_jsonbody, check_user_token

from .devicetype import devicetype_add


class DeviceType_List_Add(Resource):

    @check_jsonbody
    @check_user_token
    def post(self, user, data):
        return devicetype_add(user, data, request.args)

    # @Platform.check_usertoken(plat)
    # def get(self, user):
    #     return plat.process_devicetype_get(user, request.args)



def connect(rest_api, endpoint):
    rest_api.add_resource(DeviceType_List_Add, endpoint)
    