import urllib.parse
from .ssoaccess import sso_authorize_url, sso_token_info, sso_fetch_token

_config = dict(
    client_id='UNSET_CLIENT_ID',
    client_secret='UNSET_CLIENT_SECRET',
    sso_url='UNSET_SSO_URL',
    redirect_uri='UNSET_REDIRECT_URI'
)


def setup(app_config):
    global _config
    redirect_url = urllib.parse.urljoin(app_config['HOST_URL'], '/user/callback')
    _config = dict(
        client_id=app_config['SSO_CLIENT_ID'],
        client_secret=app_config['SSO_CLIENT_SECRET'],
        sso_url=app_config['SSO_URL'],
        redirect_uri=redirect_url
    )


def get_user_authorize_url():
    return sso_authorize_url(
        _config['client_id'],
        _config['redirect_uri'],
        _config['sso_url'],
    )


def get_user_token_info(user_token):
    status_code, token_data = sso_token_info(
        user_token,
        _config['client_id'],
        _config['client_secret'],
        _config['sso_url'],
    )

    if status_code != 200:
        # Todo: Raise exception
        return None
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
    
    token = token_data['access_token']

    return token


