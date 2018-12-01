import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import app  # noqa


class TestClient:

    def __init__(self, test_user='test_user'):

        config = {}
        config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        config['PAGE_NUM'] = 1
        config['PAGE_SIZE'] = 20
        config['DATASTORAGE_URI'] = 'mongodb://localhost:27017'
        config['MQTT_HOST'] = 'localhost'
        config['MQTT_PORT'] = 1883
        config['MQTT_USR'] = ''
        config['MQTT_PASSWORD'] = ''

        config['DEBUG'] = False
        config['TESTING'] = True

        application = app.create_app(config)
        app.db.create_all()

        self.client = application.test_client()

        if test_user:
            self._add_test_user(test_user)

    def _add_test_user(self, test_user):
        res = self.client.put('/user/add', json=dict(name=test_user))
        assert res.status_code == 200

        self.token = res.json['token']

    def _ht(self, headers={}):
        if not headers:
            return dict(userToken=self.token)

        if 'userToken' not in headers:
            headers['userToken'] = self.token
        return headers

    def post(self, endpoint, body, headers={}, **kwargs):
        headers = self._ht(headers)
        return self.client.post(endpoint, json=body, headers=headers, **kwargs)

    def put(self, endpoint, body, headers={}, **kwargs):
        headers = self._ht(headers)
        return self.client.put(endpoint, json=body, headers=headers, **kwargs)

    def get(self, endpoint, headers={}, **kwargs):
        headers = self._ht(headers)
        return self.client.get(endpoint, headers=headers, **kwargs)

    def delete(self, endpoint, headers={}, **kwargs):
        headers = self._ht(headers)
        return self.client.delete(endpoint, headers=headers, **kwargs)

    def add_devicetype(self, name, attributes={}, add_role=False, metadata=[], **kwargs):
        attr = [dict(name=n, type=k) for n, k in attributes.items()]
        d = dict(name=name, attributeTypes=attr, **kwargs)

        if 'encryptionEnabled' not in d:
            d['encryptionEnabled'] = False

        ret = self.post('/devicetype', d)
        assert ret.status_code == 200

        dt_id = ret.json['data']['id']

        if add_role:

            per_list = [dict(
                attributeTypeName=n,
                permission='N' if n in metadata else 'RW'
            ) for n, _ in attributes.items()
            ]

            dtrl = dict(
                name='device',
                deviceTypeId=dt_id,
                attributePermissions=per_list
            )

            role_ret = self.post('/role', dtrl)
            assert role_ret.status_code == 200

            return dt_id, role_ret.json['data']['id']

        return dt_id

    def clean_db(self, keep_user=True):
        app.model.DeviceType.query.delete()
        app.model.Device.query.delete()
        app.model.Role.query.delete()
        app.model.RoleGrant.query.delete()

        if not keep_user:
            app.model.User.query.delete()

        app.db.session.commit()
