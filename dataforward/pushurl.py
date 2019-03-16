from .celery import app_celery

@app_celery.task
def pushurl(url, data):
    print("You are pushing {} to {}".format(data,url))
    return (url, data)
