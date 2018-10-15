#! /usr/bin/python3
from plat import Platform


from flask_restful import Resource, Api, reqparse
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
api = Api(app)
plat = Platform('sqlite:///plat.db')

class DeviceType_Add(Resource):

    @Platform.check_jsonbody(plat)
    @Platform.check_usertoken(plat)
    def post(self, user="", data=""):
        return plat.process_devicetype_add(user, data, request.args)
    
    @Platform.check_usertoken(plat)
    def get(self, user):
        return plat.process_devicetype_get(user, request.args)

class DeviceType_Show(Resource):

    @Platform.check_jsonbody(plat)
    @Platform.check_usertoken(plat)
    def get(self, devicetypeid, user="", data=""):
        return  plat.process_devicetype_show(user, devicetypeid, request.args)

    @Platform.check_usertoken(plat)
    def delete(self, user, devicetypeid):
        return plat.process_devicetype_delete(user, devicetypeid, request.args)

class Device_List_Add(Resource):

    @Platform.check_jsonbody(plat)
    @Platform.check_usertoken(plat)
    def post(self, user="", data=""):
        return plat.process_device_add(user, data, request.args)

    @Platform.check_usertoken(plat)
    def get(self, user):
        return plat.process_device_list(user, request.args)

class Device_Show_Edit_Delete(Resource):
    @Platform.check_usertoken(plat)
    def get(self, user, deviceid):
        return plat.process_device_show(user, deviceid, request.args)

    @Platform.check_usertoken(plat)
    def delete(self, user, deviceid):
        return plat.process_device_delete(user, deviceid, request.args)

api.add_resource(DeviceType_Add  , '/devicetype') 
api.add_resource(DeviceType_Show , '/devicetype/<devicetypeid>')
api.add_resource(Device_List_Add , '/device')
api.add_resource(Device_Show_Edit_Delete, '/device/<deviceid>')

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')
