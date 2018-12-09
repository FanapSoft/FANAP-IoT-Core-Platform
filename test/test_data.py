import json
from test_client import TestClient
import unittest  # noqa
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import app  # noqa


ERROR_CODE = 500


class CheckDeviceData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tc = TestClient()

    @staticmethod
    def d2l(data_dict):
        return [dict(
            name=n,
            value=v,
        ) for n, v in data_dict.items()]

    @staticmethod
    def l2d(data_list):
        return {
            x['name']: x['value']
            for x in data_list
        }

    @staticmethod
    def send_data_to_device(data_dic, device_id):
        msg = json.dumps(dict(
            DATA=[data_dic]
        ))
        mqtt = app.get_mqtt()
        mqtt.receive_from_device(msg, device_id)

    def test_basic_usage(self):
        dt_id, device_rl = self.tc.add_devicetype('dtdd', attributes=dict(
            fsrt='String',
            fenum=['VLA1', 'VLA2'],
            fnum='Number',
            fbool='Boolean',
            mstr='String',
            mnum='Number'
        ), add_role=True,
            metadata=['mstr', 'mnum']
        )

        dev1_id, _, _ = self.tc.add_device('dev1', dt_id)
        dev2_id, _, _ = self.tc.add_device('dev2', dt_id)

        # Check accessing the device write invalid ID
        body = dict(
            attributes=self.d2l(dict(
                mstr='sdsdf',
                mnum=234
            )))
        ret = self.tc.post('/deviceData/'+dev1_id+'sdff', body)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Check accessing device-fields
        body = dict(
            attributes=self.d2l(dict(
                mstr='sdsdf',
                fnum=234
            )))
        ret = self.tc.post('/deviceData/'+dev1_id, body)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Check accessing device-fields
        body = dict(
            attributes=self.d2l(dict(
                mstr='kalam',
            )))
        ret = self.tc.post('/deviceData/'+dev1_id, body)
        self.assertEqual(ret.status_code, 200)

        cmp = dict(
            fsrt=None,
            fenum=None,
            fnum=None,
            fbool=None,
            mstr='kalam',
            mnum=None,
        )

        ret = self.tc.get('/deviceData/'+dev1_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']['attributes']
        self.assertDictEqual(cmp, self.l2d(data))

        body = dict(
            attributes=self.d2l(dict(
                mstr='Test',
                mnum=232,
            )))
        ret = self.tc.post('/deviceData/'+dev1_id, body)
        self.assertEqual(ret.status_code, 200)

        cmp = dict(
            fsrt=None,
            fenum=None,
            fnum=None,
            fbool=None,
            mstr='Test',
            mnum=232,
        )

        ret = self.tc.get('/deviceData/'+dev1_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']['attributes']
        self.assertDictEqual(cmp, self.l2d(data))
        # ###################################################

        # Check accessing the device send invalid ID
        body = dict(
            attributes=self.d2l(dict(
                fsrt='QWER',
                fenum='VLA1'
            )))
        ret = self.tc.post('/deviceData/todevice/'+dev1_id+'sdff', body)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Check accessing device-fields
        body = dict(
            attributes=self.d2l(dict(
                mnum=213,
                fbool=True
            )))
        ret = self.tc.post('/deviceData/todevice/'+dev1_id, body)
        self.assertEqual(ret.status_code, ERROR_CODE)
        # ###################################################

        # Check accessing device-fields
        body = dict(
            attributes=self.d2l(dict(
                fnum=980,
                fbool=True
            )))
        ret = self.tc.post('/deviceData/todevice/'+dev1_id, body)
        self.assertEqual(ret.status_code, 200)

        mqtt = app.get_mqtt()

        self.assertEqual(mqtt._get_tx_message_cnt(), 1)

        data = mqtt._get_last_tx_message()
        self.assertEqual(data['deviceid'], dev1_id)

        msg_dict = json.loads(data['msg'])

        self.assertListEqual(
            msg_dict['DATA'],
            [dict(fnum=980, fbool=True)]
        )
        # ###################################################

        # Sending message from device
        self.send_data_to_device(dict(
            fsrt='halooo',
            fnum=345
        ), dev1_id)

        ret = self.tc.get('/deviceData/'+dev1_id)
        self.assertEqual(ret.status_code, 200)

        cmp_dict = dict(
            fsrt='halooo',
            fenum=None,
            fnum=345,
            fbool=None,
            mstr='Test',
            mnum=232,
        )

        data = ret.json['data']['attributes']
        self.assertDictEqual(cmp_dict, self.l2d(data))
        # ###################################################

        # Try writing to the meta-field from device
        self.send_data_to_device(dict(
            mstr='zaloo',
        ), dev1_id)

        ret = self.tc.get('/deviceData/'+dev1_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']['attributes']
        self.assertDictEqual(cmp_dict, self.l2d(data))

        # Writing invalid data
        self.send_data_to_device(dict(
            fsrt=12,
            fenum='RTTT',
            fnum='Hello',
            fbool=1231,
        ), dev1_id)

        ret = self.tc.get('/deviceData/'+dev1_id)
        self.assertEqual(ret.status_code, 200)
        data = ret.json['data']['attributes']
        self.assertDictEqual(cmp_dict, self.l2d(data))
        # ###################################################

        # Define a new user for accessing from a granted device
        usr1_token = self.tc.add_user('usr_granted')

        role_id = self.tc.add_role('role-g', dt_id, dict(
            fsrt='R',
            fenum='RW',
            fnum='W',
            fbool='N',
            mstr='RW',
            mnum='N',
        ))

        self.tc.grant_role('usr_granted', dev1_id, role_id)

        # Read data from granted user
        ret = self.tc.get('/deviceData/'+dev1_id,
                          headers=dict(userToken=usr1_token))
        self.assertEqual(ret.status_code, 200)
        data = self.l2d(ret.json['data']['attributes'])

        self.assertSetEqual(set(data.keys()), set(['fsrt', 'fenum', 'mstr']))

        cmp_dict = dict(
            fsrt='halooo',
            fenum=None,
            mstr='Test',
        )

        self.assertDictEqual(cmp_dict, data)
        # ###################################################

        # ToDo: Send/Write to the fields without permission, ....


if __name__ == '__main__':
    unittest.main()
