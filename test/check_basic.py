from test_client import TestClient
import unittest  # noqa
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import app  # noqa

ERROR_CODE = 500


class CheckBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tc = TestClient()

    def setUp(self):
        self.tc.clean_db()

    @staticmethod
    def _role_d2l(data):
        return [dict(
            attributeTypeName=n,
            permission=v)
            for n, v in data.items()
        ]

    def test_adding_devicetype(self):

        dt_data = dict(
            name='dt1',
            attributeTypes=[
                dict(name='field1', type='String')
            ],
            encryptionEnabled=False,
            description='Test-Device_Type'
        )

        # Check adding simple device-type
        ret = self.tc.post('/devicetype', dt_data)
        self.assertEqual(ret.status_code, 200)
        dt_id = ret.json['data']['id']
        # ###################################################

        # Try adding devicetype with same name
        ret = self.tc.post('/devicetype', dt_data)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Check if devicetype is defined in list
        ret = self.tc.get('/devicetype')
        self.assertEqual(ret.status_code, 200)

        dt_entry = ret.json['data']['deviceTypes'][-1]
        self.assertEqual(dt_entry['id'], dt_id)
        self.assertEqual(dt_entry['name'], dt_data['name'])
        # ###################################################

        # Check getting devicetype with invalid token
        ret = self.tc.get('/devicetype/' + dt_id + 'dummy')
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Compare devicetype show with added devicetype
        ret = self.tc.get('/devicetype/' + dt_id)
        self.assertEqual(ret.status_code, 200)

        resp = ret.json

        self.assertEqual(resp['encrypted'], dt_data['encryptionEnabled'])
        self.assertEqual(resp['id'], dt_id)
        self.assertEqual(resp['description'], dt_data['description'])
        self.assertEqual(resp['name'], dt_data['name'])
        self.assertListEqual(resp['attributeTypes'], dt_data['attributeTypes'])

        # ###################################################

        # Delete dummy devicetype
        ret = self.tc.delete('/devicetype/' + dt_id + '0')
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Delete added devicetype
        ret = self.tc.delete('/devicetype/' + dt_id)
        self.assertEqual(ret.status_code, 200)

        resp = ret.json
        self.assertEqual(resp['data']['id'], dt_id)

        # Check is list of devicetypes
        ret = self.tc.get('/devicetype')
        self.assertEqual(ret.status_code, 200)
        self.assertListEqual(ret.json['data']['deviceTypes'], [])
        # ###################################################

    def test_adding_device(self):
        dt_id, rl_id = self.tc.add_devicetype('dtrol', attributes=dict(
            field1='String',
            field2=['VLA1', 'VLA2'],
            field3='Number',
            field4='Boolean'
        ), add_role=True,
            metadata=['field1', 'field3']
        )
        # ###################################################

        # >>>>>Here we have a device with role!

        # Add a new device
        dd = dict(
            name='new_device',
            label='test-label',
            deviceTypeId=dt_id
        )

        resp = self.tc.post('/device', dd)
        self.assertEqual(resp.status_code, 200)
        device_id = resp.json['data']['id']
        device_enc = resp.json['data']['encryptionKey']
        device_token = resp.json['data']['deviceToken']
        # ###################################################

        # Try adding device with same name
        resp_n = self.tc.post('/device', dd)
        self.assertEqual(resp_n.status_code, ERROR_CODE)
        # ###################################################

        # Try adding device with invalid devicetype
        dd['deviceTypeId'] = 'dummy'
        resp_n = self.tc.post('/device', dd)
        self.assertEqual(resp_n.status_code, ERROR_CODE)
        # ###################################################

        # Add a device without a device-role
        dt_id1 = self.tc.add_devicetype('dtrol1', attributes=dict(
            field1='String',
            field2=['VLA1', 'VLA2'],
            field3='Number',
            field4='Boolean'
        ), add_role=False)

        # Add a new device
        dd1 = dict(
            name='new_device1',
            label='test-label',
            deviceTypeId=dt_id1
        )

        resp = self.tc.post('/device', dd1)

        self.assertEqual(resp.status_code, ERROR_CODE)
        # ###################################################

        # Get device list
        resp = self.tc.get('/device')
        self.assertEqual(resp.status_code, 200)

        data = resp.json

        self.assertEqual(data['pageCnt'], 1)
        self.assertEqual(len(data['data']['devices']), 1)
        data = data['data']['devices'][-1]
        self.assertDictEqual(data, dict(
            isOwned=True,
            name=dd['name'],
            id=device_id
        ))
        # ###################################################

        # Show a device with dummmy device-id
        resp = self.tc.get('/device/'+device_id+'0')
        self.assertEqual(resp.status_code, ERROR_CODE)
        # ####################################################

        # Show a device details
        resp = self.tc.get('/device/'+device_id)
        self.assertEqual(resp.status_code, 200)
        data = resp.json['data']

        cmp_dict = dict(
            deviceTypeName='dtrol',
            id=device_id,
            encryptionKey=device_enc,
            name=dd['name'],
            deviceToken=device_token,
            serialNumber='',
            deviceTypeId=dt_id,
            pushURL=''
        )

        self.assertDictEqual(data, cmp_dict)
        # ####################################################

        # Try edit device with invalide device-id
        edit_body = dict(name='name-jadid!')
        resp = self.tc.put('/device/'+device_id+'0', edit_body)
        self.assertEqual(resp.status_code, ERROR_CODE)
        # ####################################################

        # Edit device by changing name

        dd = dict(
            name='new_device-01',
            label='test-label',
            deviceTypeId=dt_id
        )

        resp = self.tc.post('/device', dd)
        self.assertEqual(resp.status_code, 200)

        # First try edit name of the device (with existing name)
        edit_body = dict(name='new_device-01')
        resp = self.tc.put('/device/'+device_id, edit_body)
        self.assertEqual(resp.status_code, ERROR_CODE)

        # Rename device and serial-number
        edit_body = dict(name='esme-jadid', serialNumber='sdf234sdfs')
        resp = self.tc.put('/device/'+device_id, edit_body)
        self.assertEqual(resp.status_code, 200)

        # Compare with device show
        resp = self.tc.get('/device/'+device_id)
        self.assertEqual(resp.status_code, 200)
        data = resp.json['data']

        cmp_dict = dict(
            deviceTypeName='dtrol',
            id=device_id,
            encryptionKey=device_enc,
            name='esme-jadid',
            deviceToken=device_token,
            serialNumber='sdf234sdfs',
            deviceTypeId=dt_id,
            pushURL=''
        )

        self.assertDictEqual(data, cmp_dict)
        # ####################################################

        # Try deleting invalid device-id
        ret = self.tc.delete('/device/' + device_id + '234')
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ####################################################

        # Delete the device
        ret = self.tc.delete('/device/' + device_id)
        self.assertEqual(ret.status_code, 200)

        # List devices
        ret = self.tc.get('/device')
        self.assertEqual(ret.status_code, 200)

        data = ret.json
        self.assertEqual(data['pageCnt'], 1)
        self.assertEqual(len(data['data']['devices']), 1)
        data = data['data']['devices'][-1]
        self.assertEqual(data['name'], 'new_device-01')
        self.assertEqual(data['isOwned'], True)
        # ####################################################

        # Delete inuse devicetype
        ret = self.tc.delete('/devicetype/'+dt_id)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ####################################################

    def test_role(self):
        # Add a devicetype
        dt_id = self.tc.add_devicetype('dtrol1', attributes=dict(
            field1='String',
            field2=['VLA1', 'VLA2'],
            field3='Number',
            field4='Boolean'
        ), add_role=False,
            metadata=['field1', 'field3']
        )

        # Add a role with invalid device-id
        ret = self.tc.post('/role', dict(
            name='role1',
            deviceTypeId='2342w',
            attributePermissions=self._role_d2l(dict(field1='RW'))
        ))

        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Add a role with invalid attributeTypeName
        ret = self.tc.post('/role', dict(
            name='role1',
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(fieldXX='RW'))
        ))

        self.assertEqual(ret.status_code, ERROR_CODE)

        ret = self.tc.post('/role', dict(
            name='device',
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(field1='R'))
        ))

        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Add a valid role
        ret = self.tc.post('/role', dict(
            name='role1',
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(field1='RW', field4='N'))
        ))

        self.assertEqual(ret.status_code, 200)
        role_id = ret.json['data']['id']
        # #########################################

        # Add a role with duplicate name
        ret = self.tc.post('/role', dict(
            name='role1',
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(field1='RW', field4='N'))
        ))
        self.assertEqual(ret.status_code, ERROR_CODE)

        # #########################################

        # Generate role list
        ret = self.tc.get('/role')
        self.assertEqual(ret.status_code, 200)

        roles_list = ret.json['data']['roles']

        self.assertEqual(ret.json['pageCnt'], 1)
        self.assertEqual(len(roles_list), 1)
        self.assertDictEqual(
            roles_list[-1],
            dict(
                id=role_id,
                deviceTypeId=dt_id,
                name='role1',
                deviceTypeName='dtrol1'
            )
        )
        # #########################################

        # Show role with invalid ID
        ret = self.tc.get('/role/'+'asdfadfs')
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Show role
        ret = self.tc.get('/role/'+role_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']

        cmp_dict = dict(
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(field1='RW', field4='N')),
            description='',
            name='role1'
        )

        self.assertDictEqual(cmp_dict, data)
        # #########################################

        # Update role with invalid role-id
        ret = self.tc.put('/role/'+role_id + 'sdfdsf', {})
        self.assertEqual(ret.status_code, ERROR_CODE)

        # Update role with name='device
        ret = self.tc.put('/role/'+role_id, dict(
            name='device'
        ))
        self.assertEqual(ret.status_code, ERROR_CODE)

        ret = self.tc.post('/role', dict(
            name='role2',
            deviceTypeId=dt_id,
            attributePermissions=self._role_d2l(dict(field2='RW', field3='N'))
        ))
        self.assertEqual(ret.status_code, 200)

        # Rename role with duplicate name
        ret = self.tc.put('/role/'+role_id, dict(
            name='role2'
        ))
        self.assertEqual(ret.status_code, ERROR_CODE)

        # Check invalid attribute permissions
        ret = self.tc.put('/role/'+role_id, dict(
            attributePermissions=self._role_d2l(dict(field10='N'))
        ))
        self.assertEqual(ret.status_code, 500)
        # #########################################

        # Update role
        ret = self.tc.put('/role/'+role_id, dict(
            attributePermissions=self._role_d2l(dict(
                field1='RW'
            )),
            description='Change it',
            name='new role name'
        ))
        self.assertEqual(ret.status_code, 200)

        # Check role with show
        ret = self.tc.get('/role/'+role_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']
        cmp_dict = dict(
            attributePermissions=self._role_d2l(dict(field1='RW')),
            deviceTypeId=dt_id,
            description='Change it',
            name='new role name'
        )
        self.assertDictEqual(data, cmp_dict)
        # #########################################

        # Delete Role with invalid ID
        ret = self.tc.delete('/role/'+role_id+'00')
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Delete Role
        ret = self.tc.delete('/role/'+role_id)
        self.assertEqual(ret.status_code, 200)

        ret = self.tc.get('/role')
        self.assertEqual(ret.status_code, 200)

        data = ret.json['data']['roles']
        self.assertEqual(len(data), 1)

        data = data[-1]
        self.assertNotEqual(data['id'], role_id)
        # #########################################

    def test_rolegrant(self):
        dt_id, device_rl = self.tc.add_devicetype('dtrg', attributes=dict(
            field1='String',
            field2=['VLA1', 'VLA2'],
            field3='Number',
            field4='Boolean'
        ), add_role=True,
            metadata=['field1', 'field3']
        )

        dev_id, _, _ = self.tc.add_device('dev1', dt_id)

        usr1_token = self.tc.add_user('user1')

        role_id = self.tc.add_role('role1', dt_id, dict(
            field1='R',
            field2='RW',
            field3='W',
            field4='N',
        ))

        # Check invalid username/roleid/deviceid for grant
        d = dict(
            roleId=role_id,
            username='kalam',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id + '234',
            username='user1',
            deviceId=dev_id
        )

        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id,
            username='user1',
            deviceId=dev_id + '23423'
        )

        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id + 'xx',
            username='user1-xx',
            deviceId=dev_id + '23423'
        )

        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Granting device role
        d = dict(
            roleId=device_rl,
            username='user1',
            deviceId=dev_id
        )

        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Granting role for invalid devicetype
        dt_id1, device_rl1 = self.tc.add_devicetype('dtrg1', attributes=dict(
            field1='String',
            field2=['VLA1', 'VLA2'],
            field3='Number',
            field4='Boolean'
        ), add_role=True,
            metadata=['field1', 'field3']
        )

        role_id1 = self.tc.add_role('role1', dt_id1, dict(
            field1='R',
        ))

        d = dict(
            roleId=role_id1,
            username='user1',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Adding a valid role-grant
        d = dict(
            roleId=role_id,
            username='user1',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, 200)

        # Check multiple granting
        ret = self.tc.post('/role/grant', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Check if granted device is listed for user
        ret = self.tc.get('/device', headers=dict(userToken=usr1_token))
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.json['pageCnt'], 1)

        data = ret.json['data']['devices']

        self.assertEqual(len(data), 1)

        cmp_dict = dict(
            name='dev1',
            id=dev_id,
            isOwned=False
        )
        self.assertDictEqual(cmp_dict, data[-1])
        # #########################################

        # Get list of role grants
        ret = self.tc.get('/role/grant')
        self.assertEqual(ret.status_code, 200)

        body = ret.json
        self.assertEqual(body['pageCnt'], 1)

        role_list = body['data']['roles']
        self.assertEqual(len(role_list), 1)

        cmp_dict = dict(
            roleName='role1',
            userid='user1',
            deviceTypeName='dtrg',
            deviceId=dev_id,
            username='user1',
            deviceName='dev1',
            deviceTypeId=dt_id,
            roleId=role_id
        )

        self.assertDictEqual(cmp_dict, role_list[-1])
        # #########################################

        # Get lis of roles for granted user
        ret = self.tc.get('/role/grant', headers={"userToken": usr1_token})
        self.assertEqual(ret.status_code, 200)

        body = ret.json
        self.assertEqual(body['pageCnt'], 0)

        role_list = body['data']['roles']
        self.assertEqual(len(role_list), 0)
        # #########################################

        # Take invalid granted roleID/username/deviceid role
        d = dict(
            roleId=role_id,
            username='kalam',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id + '234',
            username='user1',
            deviceId=dev_id
        )

        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id,
            username='user1',
            deviceId=dev_id + '23423'
        )

        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)

        d = dict(
            roleId=role_id + 'xx',
            username='user1-xx',
            deviceId=dev_id + '23423'
        )

        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Try taking device role
        d = dict(
            roleId=device_rl,
            username='user1',
            deviceId=dev_id
        )

        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Take granted role
        d = dict(
            roleId=role_id,
            username='user1',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, 200)
        # #########################################

        # Retake granted role
        d = dict(
            roleId=role_id,
            username='user1',
            deviceId=dev_id
        )
        ret = self.tc.post('/role/take', d)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # #########################################

        # Check list of granted roles
        ret = self.tc.get('/role/grant')
        self.assertEqual(ret.status_code, 200)

        body = ret.json
        self.assertEqual(body['pageCnt'], 0)
        role_list = body['data']['roles']
        self.assertEqual(len(role_list), 0)
        # #########################################


if __name__ == '__main__':
    unittest.main()
