from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


def create_app(config={}):
    global application, db, CONFIG, dds
    application = Flask(__name__)

    application.config.from_mapping(config)

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

    return application


def get_dds():
    return dds
