FROM python:3.8.7-slim-buster

WORKDIR /usr/src/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/api/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/api