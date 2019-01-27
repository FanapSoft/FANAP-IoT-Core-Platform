import requests
import urllib.parse


def sso_token_info(usr_token, client_id, client_secret, sso_address):
    url = urllib.parse.urljoin(sso_address, '/oauth2/token/info')
    params = dict(token=usr_token, client_id=client_id, client_secret=client_secret)
    res = requests.post(url, params=params, headers={'Content-Type':'application/x-www-form-urlencoded'})
    
    return (res.status_code, res.json())


def sso_authorize_url(client_id, redirect_uri, sso_address):
    server = urllib.parse.urljoin(sso_address, '/oauth2/authorize')
    params = urllib.parse.urlencode(dict(
        client_id=client_id,
        response_type='code',
        redirect_uri=redirect_uri
    ))
    url = '{server}?{params}'.format(params=params, server=server)
    return url

def sso_fetch_token(client_id, client_secret, code, redirect_uri, sso_address):
    server = urllib.parse.urljoin(sso_address, '/oauth2/token/')
    params = dict(
        grant_type='authorization_code',
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret
    )
    headers = {'Content-Type':'application/x-www-form-urlencoded'}

    res = requests.post(server, headers=headers, params=params)

    return (res.status_code, res.json())


def sso_get_user_profile(token, sso_address):
    url = urllib.parse.urljoin(sso_address, '/users')
    headers = dict(
        Authorization = "Bearer {token}".format(token=token)
    )

    res = requests.get(url, headers=headers)

    return res.status_code, res.json()
