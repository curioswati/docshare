FROM python:3.6

RUN pip install pipenv

ENV PYTHONUNBUFFERED 1

RUN mkdir /docshare

WORKDIR /docshare

ADD . /docshare/

EXPOSE 8000

RUN pipenv install --ignore-pipfile

CMD export DJANGO_SUPERUSER_PASSWORD='d0c$#@r3' && pipenv run python manage.py migrate && pipenv run python manage.py createsuperuser --no-input --username "docshare-admin" --email "admin@docshare.com" && pipenv run python manage.py runserver 0.0.0.0:8000
