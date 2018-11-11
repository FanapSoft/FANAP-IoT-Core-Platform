import time
from .exception import get_ok_message_dict

def get_ok_response_body(**kwargs):
    return dict(
        timestamp = time.time(),
        message = get_ok_message_dict(),
        **kwargs,
    )
