FROM python:3.7-alpine as builder
RUN apk -U upgrade && apk add --virtual build-deps autoconf automake g++ gcc make python3-dev libffi-dev openssl-dev libmagic
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app
ENTRYPOINT [ "python3", "app.py" ]