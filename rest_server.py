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

api.add_resource(DeviceType_Add, '/devicetype') # Route_1

if __name__ == '__main__':

    app.run(debug=True)
