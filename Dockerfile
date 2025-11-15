# This Dockerfile is designed to use with provided docker-compose.yaml.

FROM python:3.13

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src src
COPY .env.docker .env

CMD python3 -m src
