from test_client import TestClient
import unittest  # noqa
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
import app  # noqa


class CheckDeviceDataModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tc = TestClient()

    def test_basic(self):
        from app.model import DeviceData
        store_data = dict(
            f_str='Hello',
            f_num=234,
            f_float=1.23,
            f_bool=False,
        )

        x = DeviceData.add_datadic('kalam_id', store_data)

        self.assertEqual(str(x['f_str']), '<kalam_id f_str=Hello>')
        self.assertEqual(str(x['f_bool']), '<kalam_id f_bool=False>')

        self.assertEqual(DeviceData.get_field_data(
            'kalam_id', 'f_str'), 'Hello')

        self.assertEqual(DeviceData.get_field_data(
            'kalam_id', 'f_float'), 1.23)

        qdata = DeviceData.get_datadict(
            'kalam_id',
            store_data.keys()
        )

        self.assertDictEqual(qdata, store_data)

    def test_multiple(self):
        from app.model import DeviceData

        DeviceData.add_datadic('id1', dict(c=True))
        DeviceData.add_datadic('id1', dict(a='Z1', b=12))
        DeviceData.add_datadic('id1', dict(b=13))
        DeviceData.add_datadic('id1', dict(a='Z34'))
        DeviceData.add_datadic('id1', dict(a='Z5'))


        # Check invalid ID
        qdata = DeviceData.get_datadict('unknown-id', ['a', 'b'])

        self.assertDictEqual(dict(a=None, b=None), qdata)

        # Query for last items plus invalid-field
        qdata = DeviceData.get_datadict('id1', list('abcd'))
        self.assertDictEqual(dict(
            a='Z5',
            b=13,
            c=True,
            d=None
        ), qdata)


if __name__ == '__main__':
    unittest.main()
