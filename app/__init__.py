from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


def create_devicdatastorage(application):
    use_mongo = application.config.get('MONGODB_FOR_DEVICE_DATA', False)

    if use_mongo:
        uri = application.config['DATASTORAGE_URI']
        from app.deviceaccess.mongo_storage import MongoStorage
        storage = MongoStorage(uri)
    else:
        from app.deviceaccess.sql_storage import DataModelStorage
        storage = DataModelStorage()

    from app.deviceaccess import DeviceDataStorage

    return DeviceDataStorage(storage)


def create_mqtt_client(application, storage):
    MockMqtt = application.config.get('MQTT_MOCK', None)
    if not MockMqtt:
        from app.deviceaccess import DAMqtt  # noqa
        d_mqtt = DAMqtt(application, storage)
        return d_mqtt
    else:
        return MockMqtt(application, storage)


def create_app(config={}):
    global application, db, CONFIG, dds, mqtt
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
    import app.authentication #noqa

    dds = create_devicdatastorage(application)

    d_mqtt = create_mqtt_client(application, dds)
    dds.set_device_sender(d_mqtt.send_to_device)
    app.authentication.setup(application.config)
    
    app.exception.register_exceptions(application)

    app.user.connect(api, '/user')
    app.devicetype.connect(api, '/devicetype')
    app.device.connect(api, '/device')
    app.role.connect(api, '/role')
    app.devicedata.connect(api, '/deviceData')

    d_mqtt.start()

    mqtt = d_mqtt

    return application


def get_dds():
    return dds


def get_mqtt():
    return mqtt
