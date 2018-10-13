import dataset
from jsonschema import validate
import json
import time
from json_check import JsonChecker

class Platform:
    ERROR_CODE=500
    ERROR_CODE_UNAUTHORIZED=401

    MSG_OK = 'MNC-M000'
    MSG_STRUCTURE_ERROR = 'MNC-M001'
    MSG_DUPLICATE_DEVICE_TYPE = 'MNC-M006'
    MSG_UNAUTHORIZED_ERROR = 'MNC-M401'


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
        with open('response_codes.json') as f:
            self.response_codes = json.load(f)['responses']

    def _generate_message_dict(self, message_code, dbg_msg=''):
        d = dict(statusCode=message_code, statusText=self.response_codes[message_code])
        if dbg_msg:
            d['dbg_message'] = dbg_msg
        return d

    def get_unique_name(self, table, column_name, prefix):
        row = table.find_one(order_by='-'+column_name)
        if not row:
            return "{}-{}".format(prefix, 0)
        
        cnt = int(row[column_name].split('-')[-1])
        return '{}-{}'.format(prefix, cnt+1)
    
    def _get_unique_devicetypeid(self):
        table = self.db.get_table('devicetype')
        return self.get_unique_name(table, 'devicetypeid', 'FNPDTID')
      
    def get_json_structure_error(self, dbg_msg=''):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_STRUCTURE_ERROR, dbg_msg)), Platform.ERROR_CODE

    def get_json_duplicate_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_DUPLICATE_DEVICE_TYPE)), Platform.ERROR_CODE

    def get_unauthorized_access_error(self):
        return dict(timeStamp=time.time(), data={}, message = self._generate_message_dict(Platform.MSG_UNAUTHORIZED_ERROR)), Platform.ERROR_CODE_UNAUTHORIZED

    def process_devicetype_add(self, payload, params):
        
        user = self.get_user_by_token(params)
        if not user:
            return self.get_unauthorized_access_error()

        payload_ok, payload_chk_msg = self.json_validator.check_devicetype_add(payload)

        if not payload_ok:
            return self.get_json_structure_error(dbg_msg=payload_chk_msg)

        # Check if device-type with same name exists
        table = self.db.get_table('devicetype')


        if table.find_one(name=payload['name'], user=user):
            return self.get_json_duplicate_error()


        if table.find_one(user=user, name = payload['name']):
            print("DeviceType exists!")

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
    


    def get_user_by_token(self, params):
        if not 'userToken' in params:
            # Token is not provided 
            return None
        

        # ToDo: Check token and get user-name
        return "todo-user"
        

    def test(self):
        return dict(kalam='sddsdsd', uri=self.database_uri, op=self.schema['devicetype_add']), 401

    
