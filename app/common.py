import time
from .exception import get_ok_message_dict
from app import CONFIG
import werkzeug.exceptions
from app.exception import ApiExp


def get_ok_response_body(**kwargs):
    return dict(
        timestamp=time.time(),
        message=get_ok_message_dict(),
        **kwargs,
    )


def paginate(q, params, fields_dict={}):

    if 'sortBy' in params:
        q = orderby_query(q, params, fields_dict)

    return page_query(q, params)


def page_query(q, params):

    page_num = params.get('pageNumber', CONFIG['PAGE_NUM'])
    page_size = params.get('pageSize', CONFIG['PAGE_SIZE'])

    try:
        ret = q.paginate(page_num, page_size)
    except werkzeug.exceptions.NotFound:
        raise ApiExp.PageNumExceed

    return ret


def orderby_query(q, params, field_dict):

    field_name = params['sortBy']

    if field_name in field_dict:
        q = q.order_by(field_dict[field_name])

    return q


def contains_string_query(q, params, param_name, field):
    if param_name in params:
        name_substr = params[param_name]
        q = q.filter(field.contains(name_substr))
    return q


def field_equal_query(q, params, param_name, collection, fieldname):

    if param_name in params:
        d = {fieldname: params[param_name]}
        q = q.filter(collection.has(**d))
    return q
