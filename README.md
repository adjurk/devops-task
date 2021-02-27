# DevOps Task

This demo Python project exposes two endpoints where only `/message` should be available for HTTP POST requests.

## Setup

To run the project in production, use `docker-compose.yml`.

```bash
$ git clone https://github.com/adjurk/devops-task && cd devops-task
# copy sample .env files
$ cp .env.sample .env & cp .env.db.sample .env.db
$ docker-compose up --build -d
# if it's your first time running the app, initialize the database
$ docker-compose exec app python manage.py create_db
```

The app is now available under 0.0.0.0:8080. To test if it's running, try making a GET request to `/`:

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
$ docker-compose exec db psql --username=postgres -d webappdb -c 'SELECT * FROM message;'

 id | message
----+---------
  1 | Test
```

## Known Issues

Due to time constraints, here are a couple of issues I've found that should be fixed in the future.

### Error Handling

- Script will not accept `Content-Type`s other than `application/json`. In case of other content type, HTTP 400 error will be returned.
- If the request JSON does not contain exactly `message` string (ex. `Message`), the script will fail and the web server will return HTTP 500 error. Other strings in request JSON are not evaluated and thus ignored.

### CRLF Issue

This should now be fixed, but sometimes after cloning, once the containers are built and started, the app container might fail with the following error message:

```
app_1    | standard_init_linux.go:219: exec user process caused: no such file or directory
devops-task_app_1 exited with code 1
```

This is due to a CRLF format that Linux won't recognize and will refuse to run the `services/web/docker-entrypoint.sh` script, resulting in container failure at start. You can fix this by converting the file from CR LF to LF.
