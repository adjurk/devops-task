FROM python:3.9-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 5000

RUN apt update && apt install -y netcat
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./services/ .

ENTRYPOINT ["/app/web/docker-entrypoint.sh"]
