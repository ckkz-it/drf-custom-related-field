FROM python:3.7-alpine

LABEL maintainer="Andrey Laguta <cirkus.kz@gmail.com>"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/app

WORKDIR /opt/app

COPY requirements.txt .

RUN apk add --no-cache \
        gcc \
        musl-dev \
        linux-headers \
        libffi-dev \
        openssl-dev \
        python3-dev \
    && rm -rf /var/cache/apk/* \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --no-cache-dir -r requirements.txt \

COPY . .

CMD ["sh"]
