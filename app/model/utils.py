import uuid


def randid(prefix, size=16):
    return prefix + str(uuid.uuid4().hex[:size])


def unique_user_token():
    return randid('TK')


def unique_devicetype_token():
    return randid('DT')


def unique_device_id():
    return randid('DI')


def unique_device_token():
    return randid('DeT', size=20)


def generate_enc_key():
    return randid('', size=32)
