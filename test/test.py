import unittest
import requests

import random



HOST = 'http://localhost:5000'
TOKEN = 'token-tavern-user'

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.host = HOST
        self.header = dict(usertoken=TOKEN)


    def test_get_device_list(self):
        res = requests.get(self.host + '/devicetype', headers=self.header)
        self.assertEqual(res.status_code, 200)

    
    def test_devicetype_add_show_list_delete(self):

        device_typename = 'test_XX2'
        device_name = 'test_device_XX2'

        ######################################################
        ## Add new devicetype and get ID
        
        attributeTypes = [dict(
                name='field-data',
                type=random.choice(['String', 'Number', 'Boolean'])
            )]
        
        payload = dict(
            name=device_typename, 
            encryptionEnabled=True,
            attributeTypes = attributeTypes
        )

        res = requests.post(self.host + '/devicetype', headers=self.header,json=payload)

        self.assertEqual(res.status_code, 200)
        
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        device_typeid = data['data']['id']


        ## Check adding duplicate devicetype
        res = requests.post(self.host + '/devicetype', headers=self.header,json=payload)
        self.assertEqual(res.status_code, 500)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M006')
        #########################################################


        ########################################################
        ## Get device-ID 
        res = requests.get(self.host + '/devicetype', headers=self.header)

        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        datatype_list = data['data']['deviceTypes']

        # Check if added device-type is enable in list
        self.assertIn(dict(id=device_typeid, name=device_typename), datatype_list)
        ########################################################

        ########################################################
        ## Get device-type information
        res = requests.get(self.host + '/devicetype/' + device_typeid , headers=self.header)

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')


        self.assertEqual(data['name'], device_typename)
        self.assertEqual(data['id'], device_typeid)
        self.assertEqual(data['encrypted'], True)


        self.assertEqual(attributeTypes, data['attributeTypes'])
        ######################################################## 


        ########################################################
        ## Add Device

        req = dict(
            name = device_name,
            deviceTypeId = device_typeid
        )

        res = requests.post(self.host + '/device', json=req , headers=self.header)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        device_id = data['data']['id']
        ######################################################## 


        ########################################################
        ## Show Device

        res = requests.get(self.host + '/device/' + device_id, headers=self.header)

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        device_data = data['data']

        self.assertEqual(device_data['id'], device_id)
        self.assertEqual(device_data['name'], device_name)
        self.assertEqual(device_data['deviceTypeId'], device_typeid)
        self.assertEqual(device_data['deviceTypeName'], device_typename)
        ######################################################## 



        ########################################################
        ## Delete Device

        res = requests.delete(self.host + '/device/' + device_id, headers=self.header)

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        self.assertEqual(data['data']['id'], device_id)
        ######################################################## 

        


        
        ########################################################
        ## Delete devicetype
        res = requests.delete(self.host + '/devicetype/' + device_typeid , headers=self.header)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M000')

        ## Try to delete deleted devicetype
        res = requests.delete(self.host + '/devicetype/' + device_typeid , headers=self.header)
        self.assertEqual(res.status_code, 500)
        data = res.json()
        self.assertEqual(data['message']['statusCode'], 'MNC-M005')

        ######################################################## 

        



if __name__ == '__main__':
    unittest.main()