FROM python:3.9-slim

EXPOSE 9000

RUN apt-get update
RUN pip3 install pipenv

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . .
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["./start"]