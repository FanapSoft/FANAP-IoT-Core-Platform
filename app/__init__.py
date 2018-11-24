from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


application = Flask(__name__)

_db_uri = 'sqlite:///plat1.db?check_same_thread=False'
application.config['SQLALCHEMY_DATABASE_URI'] = _db_uri

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PAGE_NUM'] = 1
application.config['PAGE_SIZE'] = 20
application.config['DATASTORAGE_URI'] = 'mongodb://localhost:27017'


application.config['MQTT_HOST'] = 'localhost'
application.config['MQTT_PORT'] = 1883
application.config['MQTT_USR'] = ''
application.config['MQTT_PASSWORD'] = ''


CONFIG = application.config

db = SQLAlchemy(application)
api = Api(application)

import app.user       # noqa
import app.exception  # noqa
import app.devicetype  # noqa
import app.device     # noqa
import app.role       # noqa
import app.devicedata  # noqa

from app.deviceaccess import DeviceDataStorage, DAMqtt  # noqa

dds = DeviceDataStorage(application)
d_mqtt = DAMqtt(application, dds)
dds.set_device_sender(d_mqtt.send_to_device)

app.exception.register_exceptions(application)

app.user.connect(api, '/user')
app.devicetype.connect(api, '/devicetype')
app.device.connect(api, '/device')
app.role.connect(api, '/role')
app.devicedata.connect(api, '/deviceData')


d_mqtt.start()


def get_dds():
    return dds
