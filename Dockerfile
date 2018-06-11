FROM jfloff/alpine-python:2.7

RUN apk add --no-cache libffi-dev python-dev postgresql-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app
WORKDIR /app

#Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000
