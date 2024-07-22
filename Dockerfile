FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install libpq-dev gcc -y && apt autoremove -y

RUN pip install -U pip poetry==1.8.3
RUN poetry config virtualenvs.create false

RUN mkdir /deps
WORKDIR /deps

COPY poetry.lock /deps
COPY pyproject.toml /deps

RUN poetry install
RUN rm -rf /deps

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN mkdir -p /srv/staticfiles

ENTRYPOINT ["/app/entrypoint.sh"]
