import uuid

def unique_user_token():
    return 'TK'+str(uuid.uuid4().hex[16:])
