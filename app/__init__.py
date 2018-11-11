from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


application = Flask(__name__)

_db_uri = 'sqlite:///plat1.db?check_same_thread=False'
application.config['SQLALCHEMY_DATABASE_URI'] = _db_uri

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
api = Api(application)

import app.user       # noqa
import app.exception  # noqa
import app.devicetype # noqa
import app.device     # noqa

app.exception.register_exceptions(application)

app.user.connect(api, '/user')
app.devicetype.connect(api, '/devicetype')
app.device.connect(api, '/device')
