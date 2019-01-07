#!/bin/sh

echo "Start of the platform....."
python run_server.py create_db

gunicorn -w 4 run_server:application -b :5000

