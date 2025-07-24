# Mail service
Mail service. Service developed as separate microservice.

## Stack
- [Python](https://www.python.org/)
- [celery](https://docs.celeryq.dev/en/stable/)
- [redis](https://redis.io/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [eventlet](https://pypi.org/project/eventlet/)

## Run using [docker](https://www.docker.com/)
- docker build -t <img-name> .
- docker run --name <container-name> -d <img-name>