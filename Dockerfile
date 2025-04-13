FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /srv/app

COPY requirenments.txt .

RUN pip install -U setuptools
RUN pip install --no-cache-dir -r requirenments.txt
RUN pip install gunicorn

COPY . .
RUN rm .dockerignore
RUN rm Dockerfile
RUN rm requirenments.txt