from celery import Celery


def get_brocker_addr():
    import environs
    env = environs.Env()
    with env.prefixed("RABBITMQ_"):
        usr = env("USER", "")  
        password = env("PASS", "")
        port = env("PORT","")
        host = env("URL","localhost")

    brocker_addr = 'ampq://'

    if usr:
        brocker_addr += usr
        if password:
            brocker_addr += ":" + password
        brocker_addr += '@'

    brocker_addr += host
    if port:
        brocker_addr += ":" + port

    return brocker_addr


app_celery = Celery(
    'dataforward',
    broker=get_brocker_addr(),
    include=['dataforward.pushurl']
)

if __name__ == '__main__':
    app_celery.start()

