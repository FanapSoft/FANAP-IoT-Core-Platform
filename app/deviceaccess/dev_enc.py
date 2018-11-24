import pyDes
import base64


def _create_enc_key(enc_key):
    tmp = enc_key + '00000000'

    ek = tmp[:8]
    return ek


def _get_engine(enc_key):
    ek = _create_enc_key(enc_key)
    return pyDes.des(ek, pyDes.ECB, padmode=pyDes.PAD_PKCS5)


def enc_message(msg, enc_key):
    eng = _get_engine(enc_key)
    d = eng.encrypt(msg)
    x = base64.b64encode(d)
    return x


def dec_message(msg, enc_key):
    x = base64.b64decode(msg)
    eng = _get_engine(enc_key)
    return eng.decrypt(x)
