# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9-slim-bullseye
ENV PYTHONUNBUFFERED 1

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000

# TODO: set up proper production webserver and set DEBUG to False
ENV DEBUG "True"

ARG BACKEND_URL "0.0.0.0:$PORT"
ARG FRONTEND_URL "localhost:3000"

# obviously insecure, you should pass in a better password via environment variable
ARG DJANGO_SUPERUSER_PASSWORD=admin
ARG SUPERUSER_EMAIL=admin@example.com

# For wkhtmltopdf, and install libreoffice
RUN apt update --assume-no && apt-get install libreoffice-writer-nogui libreoffice-impress-nogui libreoffice-draw-nogui wget -y --no-install-recommends \
    && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get install ./wkhtmltox_0.12.6-1.buster_amd64.deb --no-install-recommends -y \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm -rf /var/lib/apt/lists/* \
    && apt purge wget -y \
    && pip install pipenv

WORKDIR /src
COPY . ./
RUN pipenv install --system --deploy

RUN sh reset.sh

ENV BACKEND_URL ${BACKEND_URL}
ENV FRONTEND_URL ${FRONTEND_URL}

# runs the development server
CMD python manage.py runserver 0.0.0.0:$PORT
