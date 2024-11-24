# si-feedback-backend
SmartIndustry Backend code for thesis 'Research into mechanisms for collecting employee feedback'


## Run (dockerized)

```shell
$ docker-compose up --build
```


## Run (manual for dev)

```shell
$ poetry install && poetry shell
$ uvicorn src.app:app --reload 
```

## Run migrations

Go to src dir and run:

```shell
$ PYTHONPATH=.. alembic revision --autogenerate -m "some migration name"
$ PYTHONPATH=.. alembic upgrade head 
```