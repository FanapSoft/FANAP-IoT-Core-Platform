# Place all json schema checks here

import jsonschema
import json



class JsonChecker:
    def __init__(self):
        self.checkers = dict(
            devicetype_add = self._load_schema('schema_devicetype_add.json'),
            device_add = self._load_schema('schema_device_add.json'),
            role_add = self._load_schema('schema_role_add.json'),
        )


    def _validate(self, instance, schema):
        try:
            jsonschema.validate(instance, schema)
            return (True, '')
        
        except jsonschema.ValidationError as e:
            return (False, e.message)


    def check_devicetype_add(self, instance):
        schema = self.checkers['devicetype_add']
        return self._validate(instance, schema)
    
    def check_device_add(self, instance):
        schema = self.checkers['device_add']
        return self._validate(instance, schema)
    
    def check_role_add(self, instance):
        schema = self.checkers['role_add']
        return self._validate(instance, schema)
     

    def _load_schema(self, filename):
        with open(filename , 'r') as f:
            schema = json.load(f)
        return schema
