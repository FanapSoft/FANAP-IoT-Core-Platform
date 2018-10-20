#! /usr/bin/python3
from plat import Platform


from flask_restful import Resource, Api, reqparse
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
api = Api(app)
plat = Platform('sqlite:///plat.db?check_same_thread=False')

class DeviceType_List_Add(Resource):

    @Platform.check_jsonbody(plat)
    @Platform.check_usertoken(plat)
    def post(self, user="", data=""):
        return plat.process_devicetype_add(user, data, request.args)
    
    @Platform.check_usertoken(plat)
    def get(self, user):
        return plat.process_devicetype_get(user, request.args)

class DeviceType_Show_Delete(Resource):

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



#######################################################
# These endpoint is not part of API! 
# Use it for managing users
class Access_User_List(Resource):
    def get(self):
        return plat.process_list_users(request.args)
    

class Access_User_Add(Resource):
    @Platform.check_jsonbody(plat)
    def put(self, data):
        return plat.process_add_new_user(data, request.args)


api.add_resource(Access_User_List, '/users')
api.add_resource(Access_User_Add, '/users/add')

######################################################

api.add_resource(DeviceType_List_Add  , '/devicetype') 
api.add_resource(DeviceType_Show_Delete , '/devicetype/<devicetypeid>')
api.add_resource(Device_List_Add , '/device')
api.add_resource(Device_Show_Edit_Delete, '/device/<deviceid>')



if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')
