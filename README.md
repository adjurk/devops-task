# DevOps Task

This demo Python project exposes two endpoints where only `/message` should be available for HTTP POST requests.

## Setup

To run the project in production, use `docker-compose-prod.yml`.

```bash
$ git clone <this repo> && cd devops-task
$ docker-compose -f docker-compose-prod.yml up --build -d
# if it's your first time running the app, initialize the database
$ docker-compose -f docker-compose-prod.yml exec app python manage.py create_db
```

The app is now available under 0.0.0.0:8080. To test if the app works, try making a GET request to `/`:

```bash
$ curl -I -X GET localhost:8080/

HTTP/1.1 405 Not Allowed
Server: nginx/1.17.10
Date: Fri, 19 Feb 2021 09:48:13 GMT
Content-Type: text/html
Content-Length: 158
Connection: keep-alive
```

## Running

Nginx container should handle and block all GET requests like the one above. The Python app has a `/message` endpoint that accepts an `application/json` body that looks like this:

```json
{
    "message": "Here goes your message"
}
```

Here's an example POST request:

```bash
$ curl -L -X POST localhost:8080/message -H 'Content-Type: application/json' -d '{ "message": "Test" }'

{"result":"Message saved successfully."}
```

You can check the database by connecting directly to the container (PostgreSQL is not exposed outside Docker network) using docker-compose:

```bash
docker-compose -f docker-compose-prod.yml exec db psql --username=postgres -d webappdb -c 'SELECT * FROM message;'
```
