from .celery import app_celery
import requests
import time

@app_celery.task
def pushurl(url, data):
    ret = requests.post(url, json=data, timeout=4)
    result = [time.time(), url, data, ret.status_code, ret.text]
    print(result)
    return result
