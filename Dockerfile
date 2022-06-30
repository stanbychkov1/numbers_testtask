FROM python:3.8.3-slim-buster

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY . .
ENTRYPOINT ["/docker-entrypoint.sh"]