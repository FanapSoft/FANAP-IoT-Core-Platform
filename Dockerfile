FROM python:3.7-alpine
COPY requirements.txt /
RUN pip install gunicorn
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 5000

ENTRYPOINT [ "gunicorn" ] 
CMD [ "-w", "4", "run_server:application", "-b", ":5000" ]

