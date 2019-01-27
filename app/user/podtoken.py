from flask import render_template, Response, redirect
import requests

import app.authentication

def userlogin():
    return redirect(
        app.authentication.get_user_authorize_url()
    )


def callback(url_args):

    code = url_args['code']
    
    token = app.authentication.fetch_token_for_user(code)

    if token==None:
        token = 'INVALID!'

    return Response(render_template('token.html', token=token),mimetype='text/html')



