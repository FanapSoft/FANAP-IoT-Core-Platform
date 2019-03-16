from celery import Celery

app_celery = Celery(
    'dataforward',
    broker='amqp://guest:guest@localhost',
    include=['dataforward.pushurl']
)

if __name__ == '__main__':
    app_celery.start()

