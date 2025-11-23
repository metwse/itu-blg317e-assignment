# This docker file is for running standalone database instances quickly.

FROM postgres:16

ENV POSTGRES_DB=blg317e
ENV POSTGRES_USER=dbuser
ENV POSTGRES_PASSWORD=insecure-password_NO-NOT-EXPOSE-THIS-DB-TO-PUBLIC

COPY *.sql /docker-entrypoint-initdb.d/
