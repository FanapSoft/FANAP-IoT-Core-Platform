from flask import render_template, Response, redirect, render_template_string
import requests

import app.authentication

def userlogin():
    return redirect(
        app.authentication.get_user_authorize_url()
    )


def callback(url_args):

    code = url_args['code']
    
    token_data = app.authentication.fetch_token_for_user(code)

    if token_data==None:
        return Response(
            render_template_string("Unable to get token from SSO....")
        )

    auth_cfg = app.authentication.get_config_dict()

    params = dict(
        client_id = auth_cfg['client_id'],
        client_secret = auth_cfg['client_secret'],
        refresh_token = token_data['refresh_token'],
        token = token_data['access_token'],
        expires_in = token_data['expires_in'],
        sso_url = auth_cfg['sso_url']+'/oauth2/token',
    )

    return Response(render_template('token.html', **params),mimetype='text/html')

