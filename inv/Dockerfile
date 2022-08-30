FROM python:3-slim-buster

WORKDIR /inv


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /inv

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
