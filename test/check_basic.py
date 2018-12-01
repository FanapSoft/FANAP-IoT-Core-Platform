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


if __name__ == '__main__':
    unittest.main()
