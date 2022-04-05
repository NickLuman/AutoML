FROM python:3.9.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# COPY pyproject.toml alembic.ini poetry.lock /code
COPY pyproject.toml poetry.lock .env /code
RUN poetry install --no-dev

COPY src /code/src
# COPY  alembic  /code/alembic

# CMD ["uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]