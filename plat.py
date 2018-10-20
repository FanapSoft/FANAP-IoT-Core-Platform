import dataset
from jsonschema import validate
import json
import time
from json_check import JsonChecker
import random

from flask import request


class Platform:
    ERROR_CODE=500
    ERROR_CODE_UNAUTHORIZED=401

    MSG_OK = 'MNC-M000'
    MSG_STRUCTURE_ERROR = 'MNC-M001'
    MSG_DUPLICATE_DEVICE_TYPE = 'MNC-M006'
    MSG_DUPLICATE_DEVICE = 'MNC-M009'
    MSG_UNAUTHORIZED_ERROR = 'MNC-M401'
    MSG_DEVICETYPEID_NOTFOUND = 'MNC-M005'
    MSG_DEVICETYPE_INUSE = 'MNC-M007'
    MSG_DEVICE_NOTFOUND = 'MNC-M008'


    def __init__(self, database_uri):
        self.db = dataset.connect(database_uri)
        self.database_uri = database_uri
        self.load_json_schema()
        self.load_response_codes()
        self.json_validator = JsonChecker()

    def load_json_schema(self):
        self.schema = {}
        
        with open('schema_devicetype_add.json') as f:
            self.schema['devicetype_add'] = json.load(f)


    def load_response_codes(self):
        with open('response_codes.json', encoding='utf-8') as f:
            self.response_codes = json.load(f)['responses']

    def _generate_message_dict(self, message_code, dbg_msg=''):
        d = dict(statusCode=message_code, statusText=self.response_codes[message_code])
        if dbg_msg:
            d['dbg_message'] = dbg_msg
        return d

    def get_unique_name(self, table, column_name, prefix):
        row = table.find_one(order_by='-'+column_name)
        if not row:
            return "{}-{:09}".format(prefix, 0)
        
        cnt = int(row[column_name].split('-')[-1])
        return '{}-{:09}'.format(prefix, cnt+1)
    
    def _get_unique_devicetypeid(self):
        table = self.db.get_table('devicetype')
        return self.get_unique_name(table, 'devicetypeid', 'FNPDTID')
      
    def _get_unique_deviceid(self):
        table = self.db.get_table('device')
        return self.get_unique_name(table, 'deviceid', 'FNPDEV')

    def _gen_enc_key(self):
        return ''.join([random.choice('0123456789ABCDEF') for x in range(8)])

    def _gen_device_token(self):
        return 'token-{}'.format(''.join([random.choice('0123456789ABCDEF') for x in range(4)]))


    def get_json_structure_error(self, dbg_msg=''):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_STRUCTURE_ERROR, dbg_msg)), Platform.ERROR_CODE

    def get_json_duplicate_devicetype_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DUPLICATE_DEVICE_TYPE)), Platform.ERROR_CODE

    def get_json_duplicate_device_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DUPLICATE_DEVICE)), Platform.ERROR_CODE

    def get_unauthorized_access_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_UNAUTHORIZED_ERROR)), Platform.ERROR_CODE_UNAUTHORIZED

    def get_devicetype_not_found_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DEVICETYPEID_NOTFOUND)), Platform.ERROR_CODE

    def get_device_not_found(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DEVICE_NOTFOUND)), Platform.ERROR_CODE

    def get_devicetype_inuse_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DEVICETYPE_INUSE)), Platform.ERROR_CODE
        

    def _get_by_devicetypeid(self, devicetypeid):
        table = self.db.get_table('devicetype')
        res = table.find_one(devicetypeid=devicetypeid)   
        return res  

    def _get_by_deviceid(self, deviceid):
        table = self.db.get_table('device')
        res = table.find_one(deviceid=deviceid)   
        return res  

    def process_devicetype_add(self, user, payload, params):
        payload_ok, payload_chk_msg = self.json_validator.check_devicetype_add(payload)

        if not payload_ok:
            return self.get_json_structure_error(dbg_msg=payload_chk_msg)

        # Check if device-type with same name exists
        table = self.db.get_table('devicetype')


        if table.find_one(name=payload['name'], user=user):
            return self.get_json_duplicate_devicetype_error()

        new_devtype_id = self._get_unique_devicetypeid()

        description = payload.get('description', '')

        table.insert( dict(
            name = payload['name'],
            enc_en = payload['encryptionEnabled'],
            description = description,
            user = user,
            devicetypeid= new_devtype_id,
            devicetype = json.dumps(dict(data=payload['attributeTypes']))
            ))


        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK), 
            data = {"id":new_devtype_id},
            )
    
    def process_devicetype_get(self, user, params):
        # Check if device-type with same name exists
        table = self.db.get_table('devicetype')     

        devicetype_list = [dict(id=x['devicetypeid'], name=x['name']) for x in table.find(user=user)]


        if 'name' in params:
            substr = params['name']
            
            devicetype_list = list(filter(lambda x: substr in x['name'], devicetype_list))

        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK), 
            data = {'deviceTypes':devicetype_list},
        )       
    
    def process_devicetype_show(self, user, devicetypeid, params):
        res = self._get_by_devicetypeid(devicetypeid)
        if not res:
            return self.get_devicetype_not_found_error()
        

        devtype = json.loads(res['devicetype'])['data']

        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK),             
            name = res['name'],
            encrypted=res['enc_en'],
            id = devicetypeid,
            description = res['description'],
            attributeTypes = devtype,
        )

    def process_devicetype_delete(self, user, devicetypeid, params):
        table = self.db.get_table('devicetype')

        res = self._get_by_devicetypeid(devicetypeid)
        if not res:
            return self.get_devicetype_not_found_error()


        device_table = self.db.get_table('device')

        if device_table.find_one(devicetypeide=devicetypeid):
            return self.get_devicetype_inuse_error()

        ret_value = dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK),             
            data = dict(id = devicetypeid),
        )     

        table.delete(devicetypeid=devicetypeid)
        return ret_value 

    def process_device_add(self, user, payload, params):
        payload_ok, payload_chk_msg = self.json_validator.check_device_add(payload)

        if not payload_ok:
            return self.get_json_structure_error(dbg_msg=payload_chk_msg)
        
        devicetypeid = payload['deviceTypeId']

        devicetype_entry = self._get_by_devicetypeid(devicetypeid)
        if not devicetype_entry:
            return self.get_devicetype_not_found_error()

        # Check if device with same name exists
        table = self.db.get_table('device')

        if table.find_one(name=payload['name'], user=user):
            return self.get_json_duplicate_device_error()


        serialNumber = params.get('serialNumber','')

        new_device_id = self._get_unique_deviceid()
        encryptionkey = self._gen_enc_key()
        token = self._gen_device_token()

        table.insert( dict(
            name = payload['name'],
            deviceid=new_device_id,
            devicetypeide = devicetypeid,
            enc_key = encryptionkey,
            user = user,
            device_token = token,
            serial_number = serialNumber,
            ))

        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK),             
            data = dict(
                id = new_device_id,
                encryptionKey = encryptionkey,
                deviceToken = token
            )
        )

    def process_device_list(self, user, params):
        # Check if device-type with same name exists
        table = self.db.get_table('device')     

        device_list = [dict(id=x['deviceid'], name=x['name']) for x in table.find(user=user)]


        if 'name' in params:
            substr = params['name']
            
            device_list = list(filter(lambda x: substr in x['name'], device_list))

        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK), 
            data = {'devices':device_list},
        )  

    def process_device_show(self, user, deviceid, params):
        table = self.db.get_table('device')

        res = self._get_by_deviceid(deviceid)
        if not res:
            return self.get_device_not_found()

        devicetype_id = res['devicetypeide']
        devicetype_entry = self._get_by_devicetypeid(devicetype_id)
        devicetype_name = devicetype_entry['name']

        return dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK), 
            data = dict(
                id = deviceid,            
                name = res['name'],
                deviceTypeId = devicetype_id,
                deviceTypeName = devicetype_name,
                serialNumber = res['serial_number'],
                encryptionKey = res['enc_key'],
                deviceToken = res['device_token'],
            ),
        )

    def process_device_delete(self, user, deviceid, params):
        table = self.db.get_table('device')

        res = self._get_by_deviceid(deviceid)
        if not res:
            return self.get_device_not_found()

        ret_value = dict(
            timestamp=time.time(),  
            message = self._generate_message_dict(Platform.MSG_OK),             
            data = dict(id = deviceid),
        )     

        table.delete(deviceid=deviceid)
        return ret_value 
    
    def process_list_users(self, params):
        table = self.db.get_table('user')

        usr_itr = table.find(order_by='name')

        return dict(
            timestamp=time.time(),
            users = [dict(name=x['name'], token=x['token']) for x in usr_itr]
        )
    
    def process_add_new_user(self, data, params):
        user_name = data.get('name', None)
        
        if not user_name:
            return dict(message='User name is not provided'), 401
        
        table = self.db.get_table('user')

        if table.find_one(name=user_name):
            return dict(message='User exists'), 401
        
        #token = ''.join([random.choice('0123456789ABCDEF') for x in range(12)])
        token = 'token-' + user_name

        table.insert(dict(name=user_name, token = token))

        return dict(message='User created', name=user_name, token=token)


    def check_user_by_token(self, token):
        if not token:
            return None
        
        table = self.db.get_table('user')

        u_row = table.find_one(token=token)

        if not u_row:
            return None
        
        return u_row['name']

    


    def check_usertoken(platform):
        def decorator_wrapper(func):
            def wrapper(self, *args, **kargs):
                user = platform.check_user_by_token(request.headers.get('userToken'))
                if not user:
                    return platform.get_unauthorized_access_error()
                
                return func(self, *args, user=user, **kargs)
            
            return wrapper
        return decorator_wrapper
    

    def check_jsonbody(platform):
        def decorator_wrapper(func):
            def wrapper(self, *args, **kargs):
                try:
                    data = request.get_json()
                except:
                    return platform.get_json_structure_error()

                return func(self, *args, data=data, **kargs)
            
            return wrapper
        return decorator_wrapper
