#! /usr/bin/python3
from plat import Platform

from flask_restful import Resource, Api, reqparse
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
api = Api(app)
    
plat = Platform('sqlite:///plat.db')

class DeviceType_Add(Resource):

    def post(self):
        try:
            data = request.get_json()
        except:
            return plat.get_json_structure_error()

        return plat.process_devicetype_add(data, request.args)
    
    def get(self):
        return plat.process_devicetype_get(request.args)

class DeviceType_Show(Resource):

    def get(self, devicetypeid):
        return  plat.process_devicetype_show(devicetypeid, request.args)

    def delete(self, devicetypeid):
        return plat.process_devicetype_delete(devicetypeid, request.args)

class Device_List_Add(Resource):
    def post(self):
        try:
            data = request.get_json()
        except:
            return plat.get_json_structure_error()

        
        return plat.process_device_add(data, request.args)

    def get(self):
        return plat.process_device_list(request.args)


class Device_Show_Edit_Delete(Resource):
    def get(self, deviceid):
        return plat.process_device_show(deviceid, request.args)

    def delete(self, deviceid):
        return plat.process_device_delete(deviceid, request.args)

api.add_resource(DeviceType_Add  , '/devicetype') 
api.add_resource(DeviceType_Show , '/devicetype/<devicetypeid>')
api.add_resource(Device_List_Add , '/device')
api.add_resource(Device_Show_Edit_Delete, '/device/<deviceid>')

if __name__ == '__main__':

    app.run(debug=True)
