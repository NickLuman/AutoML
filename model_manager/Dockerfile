FROM python:3.9.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean


ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

WORKDIR src

ENV LANG C.UTF-8
COPY src src

# EXPOSE 8000

# CMD ["uvicorn", "src.__main__:app", "--host", "0.0.0.0", "--port", "8000"]