#!/bin/bash
export LC_ALL=en_US.utf8
pip install -r requirements.txt
# python manage.py collectstatic
# python manage.py migrate
nohup uwsgi --ini uwsgi.ini
