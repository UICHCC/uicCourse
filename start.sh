#!/bin/sh

python manage.py makemigrations && python manage.py migrate && gunicorn uicCourse.wsgi -t 60 -b 0.0.0.0:5002
