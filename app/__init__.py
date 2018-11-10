from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api



application =Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plat1.db?check_same_thread=False'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
api = Api(application)

import app.user
import app.exception
import app.devicetype

app.exception.register_exceptions(application)

app.user.connect(api, '/user')
app.devicetype.connect(api, '/devicetype')