#!/bin/bash
export LC_ALL=en_US.utf8
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
nohup uwsgi --ini uwsgi.ini
