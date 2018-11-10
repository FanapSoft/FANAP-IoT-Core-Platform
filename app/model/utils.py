import uuid


def randid(prefix, size=16):
    return prefix + str(uuid.uuid4().hex[size:])

def unique_user_token():
    return randid('TK')


def unique_devicetype_token():
    return randid('DT')
