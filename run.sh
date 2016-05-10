#!/bin/sh
#gunicorn -b 0.0.0.0:80 -k gevent webapp.wsgi
nohup gunicorn --reload -k gevent web.wsgi >stdout.log 2>&1  &
