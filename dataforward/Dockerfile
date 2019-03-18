FROM python:3.7-alpine


RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

RUN mkdir /app/dataforward
COPY . /app/dataforward
WORKDIR /app

ENTRYPOINT [ "celery" ] 
CMD [ "-A", "dataforward", "worker", "-l", "info", "--concurrency=5"]

