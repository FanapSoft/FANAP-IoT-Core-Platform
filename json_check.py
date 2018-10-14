# Place all json schema checks here

import jsonschema
import json



class JsonChecker:
    def __init__(self):
        self.checkers = dict(
            devicetype_add = self._load_schema('schema_devicetype_add.json'),
            device_add = self._load_schema('schema_device_add.json'),
        )

    def check_devicetype_add(self, instance):
        schema = self.checkers['devicetype_add']
        try:
            jsonschema.validate(instance, schema)
            return (True, '')
        
        except jsonschema.ValidationError as e:
            return (False, e.message)
    
    def check_device_add(self, instance):
        schema = self.checkers['device_add']
        try:
            jsonschema.validate(instance, schema)
            return (True, '')
        
        except jsonschema.ValidationError as e:
            return (False, e.message)
            

    def _load_schema(self, filename):
        with open(filename , 'r') as f:
            schema = json.load(f)
        return schema
