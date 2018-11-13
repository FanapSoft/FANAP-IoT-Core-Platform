import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app import application  # noqa
from app.exception import ApiExp  # noqa
import unittest  # noqa
import uuid  # noqa


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.client = application.test_client()
        self._setup_test_users()

    def _add_user(self, username):
        res = self.client.put('/user/add', json=dict(name=username))
        return res.json['token']

    def _add_devicetype(self, usertoken, name, enc, fielddict, desciption=''):
        attribute_list = [dict(name=n, type=t) for n, t in fielddict.items()]

        body = dict(name=name, encryptionEnabled=enc,
                    attributeTypes=attribute_list)

        if desciption:
            body['desciption'] = desciption

        res = self.client.post('/devicetype', json=body,
                               headers=dict(userToken=usertoken))

        return res.json

    def _add_device(self, usertoken, dt_id, name, **kwargs):

        body = dict(
            name=name,
            deviceTypeId=dt_id,
            **kwargs,
        )

        res = self.client.post('/device', json=body,
                               headers=dict(userToken=usertoken))

        return res.json

    def _add_role(self, usertoken, name, devicetype, attrib_dict, description=''):

        attribute_list = [dict(attributeTypeName=n, permission=t)
                          for n, t in attrib_dict.items()]

        body = dict(name=name, deviceTypeId=devicetype,
                    attributePermissions=attribute_list)
        if description:
            body['description'] = description

        res = self.client.post('/role', json=body,
                               headers=dict(userToken=usertoken))

        return res.json

    def _add_rolegrant(self, usertoken, granted_user, role, device, take=False):
        body = dict(
            username=granted_user,
            roleId=role,
            deviceId=device
        )

        if take:
            ep = '/role/take'
        else:
            ep = '/role/grant'

        res = self.client.post(ep, json=body,
                               headers=dict(userToken=usertoken))

        return res.json

    def _get_rolegrant_list(self, usertoken):
        res = self.client.get('/role/grant', headers=dict(userToken=usertoken))
        return res.json

    def _setup_test_users(self):
        self.username1 = 'usr1-' + uuid.uuid4().hex[:10]

        self.username2 = 'usr2-' + uuid.uuid4().hex[:10]

        self.usertoken1 = self._add_user(self.username1)
        self.usertoken2 = self._add_user(self.username2)

    def test_datasetup(self):

        dt1 = self._add_devicetype(self.usertoken1, 'Datatyp1', True, dict(
            temp='String',
            value='Number',
            status=['State1', 'State2']
        ))

        dt2 = self._add_devicetype(self.usertoken1, 'Datatyp2', True, dict(
            temp='String',
            troze='String',
            blan='Boolean',
            value='Number',
            status=['State1', 'State2']
        ))

        dt1_id = dt1['data']['id']
        dt2_id = dt2['data']['id']

        dr1 = self._add_role(self.usertoken1, 'device', dt1_id, {'temp': 'RW'})
        dr2 = self._add_role(self.usertoken1, 'device', dt2_id, {'troze': 'N'})

        d1 = self._add_device(self.usertoken1, dt1_id, 'Device1')
        d1_1 = self._add_device(self.usertoken1, dt1_id, 'Device11')
        d2 = self._add_device(self.usertoken1, dt2_id, 'Device2')

        d1_id = d1['data']['id']
        d2_id = d2['data']['id']
        d11_id = d1_1['data']['id']

        role1 = self._add_role(self.usertoken1, 'role1',
                               dt1_id, {'value': 'R'})

        rl1_id = role1['data']['id']

        rg1 = self._add_rolegrant(
            self.usertoken1, self.username2, rl1_id, d1_id)

        # # Add duplicate role
        # with self.assertRaises(ApiExp.RoleAlreadyGranted):
        #     rg2 = self._add_rolegrant(self.usertoken1, self.username2, rl1_id, d1_id)

        # Create wrong grant

        # rg1 = self._add_rolegrant(self.usertoken1, self.username2, rl1_id, d2_id)

        rg2 = self._add_rolegrant(
            self.usertoken1, self.username2, rl1_id, d11_id)

        x = self._get_rolegrant_list(self.usertoken1)
        print(x['data'])

        dr1 = self._add_rolegrant(
            self.usertoken1, self.username2, rl1_id, d1_id, take=True)

        x = self._get_rolegrant_list(self.usertoken1)
        print(x['data'])


if __name__ == '__main__':
    unittest.main()
