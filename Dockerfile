FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /ems_web

WORKDIR /ems_web

COPY . /ems_web/

RUN pip install --upgrade pip

RUN pip install -r config/requirements/mysql_db.txt
