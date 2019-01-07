#! /usr/bin/python3
import app
from pathlib import Path
import sys
import os
import app.envparser


DB_FILE = 'plat.db'


def create_config_dict():
    # Here create configurations using OS environment variables with default values

    db_uri = 'sqlite:///{}?check_same_thread=False'.format(
        Path(__file__).parent.absolute() / DB_FILE
    )

    return app.envparser.build([
        ('SQLALCHEMY_DATABASE_URI', db_uri),
        ('SQLALCHEMY_TRACK_MODIFICATIONS', False, 'bool'),
        ('PAGE_NUM', 1, 'int'),
        ('PAGE_SIZE', 20, 'int'),
        ('MONGODB_FOR_DEVICE_DATA', False, 'bool'),
        ('DATASTORAGE_URI', 'mongodb://localhost:27017'),
        ('MQTT_HOST', 'localhost'),
        ('MQTT_PORT', 1883, 'int'),
        ('MQTT_USR',),
        ('MQTT_PASSWORD',),
    ])


def create_db():
    print('Create database!')
    app.db.create_all()


config = create_config_dict()

application = app.create_app(config)

if 'create_db' in sys.argv:
    create_db()
    exit(0)


if __name__ == '__main__':

    application.run(debug=True, host='0.0.0.0')
