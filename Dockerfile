FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install gunicorn
RUN pip install -r /requirements.txt
RUN apk add libpq
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && apk del --no-cache .build-deps

RUN mkdir /app
COPY . /app
WORKDIR /app
EXPOSE 5000

ENTRYPOINT [ "gunicorn" ] 
CMD [ "-w", "4", "run_server:application", "-b", ":5000" ]

