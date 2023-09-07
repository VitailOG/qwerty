FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache libffi-dev gcc musl-dev postgresql-dev python3-dev postgresql-client

COPY requirements.txt .

RUN pip install cffi

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

COPY . .