#FROM python:3.8-slim-buster
FROM alpine:3.14

RUN apk add python3 \
    && apk add python3-dev \
    && apk add musl-dev \
    && apk add py3-pip

RUN apk add gcc

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED 1
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "1", "xmrsale:app"]

