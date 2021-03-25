FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /docshare

WORKDIR /docshare

ADD . /docshare/

EXPOSE 8000

RUN pipenv install

ENTRYPOINT ["python", "docshare/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
