from pymongo import MongoClient


class MongoStorage:
    DB_NAME = 'devicedata'

    def __init__(self, db_uri):
        db_client = MongoClient(db_uri)
        self.db = db_client[MongoStorage.DB_NAME]

    def read_data(self, field_list, deviceid):
        ret = {}
        for field in field_list:
            q = self.query_last_field(field, deviceid)
            if not q:
                ret[field] = None
            else:
                ret[field] = q[0][field]
        return ret

    def query_last_field(self, field_name, deviceid):

        c = self.db[deviceid]

        return list(
            c.find({field_name: {"$exists": True}}).hint(
                [('$natural', -1)]).limit(1)
        )

    def store_data(self, data, deviceid):
        if type(data) not in [list, tuple]:
            data = [data]

        # Get device collection
        collection = self.db[deviceid]

        collection.insert_many(data)
