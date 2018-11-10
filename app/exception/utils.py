from flask import jsonify
import time
import inspect

from .exceptions import get_message
from .exceptions import ApiExp
from .exceptions import ErrorStatusCode


default_status_code = ErrorStatusCode

def generate_response(exception_class):
    payload = dict()
    if hasattr(exception_class, 'payload'):
        payload = exception_class.payload

    status_code = default_status_code
    if hasattr(exception_class, 'status_code'):
        status_code = exception_class.status_code

    ret_dict = dict(
        timeStamp = time.time(),
        data = {},
        message = dict(
            statusCode=exception_class.msg_id,
            statusText= get_message(exception_class.msg_id),
        ),
        **payload
    )

    return jsonify(ret_dict), status_code


def register_exceptions(app):

    for c in _get_class_list():
        app.register_error_handler(c, lambda x: generate_response(x))


def _get_class_list():
    return filter(inspect.isclass, ApiExp.__dict__.values())
