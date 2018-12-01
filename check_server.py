#! /usr/bin/python3
import app
from pathlib import Path
import sys
import os


def create_db():
    print("Creating default database!")
    app.db.create_all()


if __name__ == '__main__':

    DB_FILE = 'plat.db'

    config = {}

    _db_uri = 'sqlite:///{}?check_same_thread=False'.format(
        Path(__file__).parent.absolute() / DB_FILE
    )

    config['SQLALCHEMY_DATABASE_URI'] = _db_uri

    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config['PAGE_NUM'] = 1
    config['PAGE_SIZE'] = 20
    config['DATASTORAGE_URI'] = 'mongodb://localhost:27017'

    config['MQTT_HOST'] = 'localhost'
    config['MQTT_PORT'] = 1883
    config['MQTT_USR'] = ''
    config['MQTT_PASSWORD'] = ''

    application = app.create_app(config)

    if 'create_db' in sys.argv:
        create_db()
        exit(0)

    if not os.path.isfile(DB_FILE):
        create_db()

    application.run(debug=True, host='0.0.0.0')
