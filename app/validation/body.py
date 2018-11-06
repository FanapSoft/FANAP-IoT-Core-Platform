from app.exception import ApiExp
from flask import request

# Validate json body



def check_jsonbody(func):
    def wrapper(self, *args, **kargs):
        try:
            data = request.get_json()
        except:
            raise ApiExp.Structural

        return func(self, *args, data=data, **kargs)        
    return wrapper