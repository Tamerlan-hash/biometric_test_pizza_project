FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /pizza

COPY ./requirements.txt /pizza/requirements.txt

RUN apk add build-base

RUN pip install --upgrade -r /pizza/requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--workers=2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
