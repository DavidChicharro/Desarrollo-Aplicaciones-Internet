FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add supervisor

# Creating working directory inside container
RUN mkdir /web
COPY . /web
COPY gunicorn.ini /etc/supervisor.d/

WORKDIR /web
RUN pip3 install -r requirements.txt
