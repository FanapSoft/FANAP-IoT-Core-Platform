# Setup Application in Flask rest framework

from flask_restful import Resource
from app.validation import check_jsonbody


class Access_User_List(Resource):
    def get(self):
        # return plat.process_list_users(request.args)
        return dict(msg='User List')
    

class Access_User_Add(Resource):
    # @Platform.check_jsonbody(plat)
    # def put(self, data):
    #     return plat.process_add_new_user(data, request.args)

    @check_jsonbody
    def put(self, data):
        return dict(msg='This is User ADD', data=data)




def connect(rest_api, endpoint):
    rest_api.add_resource(Access_User_List, endpoint)
    rest_api.add_resource(Access_User_Add, endpoint + '/add')
    