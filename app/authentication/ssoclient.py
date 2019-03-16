import urllib.parse
import time
from .ssoaccess import sso_authorize_url, sso_token_info, sso_fetch_token, sso_get_user_profile

_config = dict(
    client_id='UNSET_CLIENT_ID',
    client_secret='UNSET_CLIENT_SECRET',
    sso_url='UNSET_SSO_URL',
    redirect_uri='UNSET_REDIRECT_URI',
    cache_client=None,
)


def setup(app_config):
    global _config
    redirect_url = urllib.parse.urljoin(app_config['HOST_URL'], '/user/callback')
    cache_client = None
    if app_config['USE_TOKEN_CACHE']:
        import redis
        cache_client = redis.Redis(host=app_config['REDIS_URL'], port=app_config['REDIS_PORT'])

    _config = dict(
        client_id=app_config['SSO_CLIENT_ID'],
        client_secret=app_config['SSO_CLIENT_SECRET'],
        sso_url=app_config['SSO_URL'],
        redirect_uri=redirect_url,
        cache_client=cache_client,
    )

    print(_config['cache_client'])


def get_user_authorize_url():
    return sso_authorize_url(
        _config['client_id'],
        _config['redirect_uri'],
        _config['sso_url'],
    )

def _convert_to_str(data):
    if isinstance(data, bytes):      return data.decode()
    if isinstance(data, (str, int)): return str(data)
    if isinstance(data, dict):       return dict(map(_convert_to_str, data.items()))
    if isinstance(data, tuple):      return tuple(map(_convert_to_str, data))
    if isinstance(data, list):       return list(map(_convert_to_str, data))
    if isinstance(data, set):        return set(map(_convert_to_str, data))


def _cache_store_tokendata(user_token, token_data, cache_client):
    if token_data['active']:
        store_data = dict(active=int(token_data['active']), sub=token_data['sub'])
        cache_client.hmset(user_token, store_data)
        ex_time = int(token_data['exp']-time.time())
        ex_time = int(ex_time/100)
        cache_client.expire(user_token, ex_time)
        return store_data
    return None

def get_user_token_info(user_token):
    cache_client = _config['cache_client']

    token_data = {}
    if cache_client:
        token_data = _convert_to_str(cache_client.hgetall(user_token))

    if not token_data:
        status_code, token_data = sso_token_info(
            user_token,
            _config['client_id'],
            _config['client_secret'],
            _config['sso_url'],
        )
        if status_code != 200:
            # Todo: Raise exception
            return None

        if cache_client:
            _cache_store_tokendata(user_token, token_data, cache_client)
            

        return token_data
    else:
        return token_data



def fetch_token_for_user(code):
    status, token_data = sso_fetch_token(
        _config['client_id'],
        _config['client_secret'],
        code,
        _config['redirect_uri'],
        _config['sso_url'],
    )

    if status != 200:
        return None
    
    return token_data


def get_user_profile(user_token):
    status, profile = sso_get_user_profile(
        user_token,
        _config['sso_url']
    )

    if status != 200:
        return None
    
    return profile

def get_config_dict():
    return _config