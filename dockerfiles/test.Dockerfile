FROM python:3.8-alpine

WORKDIR /work

COPY requirements/test.txt /tmp/requirements/test.txt

RUN pip install -r /tmp/requirements/test.txt --no-cache-dir
