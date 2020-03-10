FROM python:3.7-alpine

LABEL maintainer="Andrey Laguta <cirkus.kz@gmail.com>"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --no-cache-dir -r requirements.txt

COPY drf_custom_related_field .
COPY tests .

CMD ["sh"]
