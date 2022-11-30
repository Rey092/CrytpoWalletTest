FROM python:3.8

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app


RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl

# Upgrade pip
RUN pip install --upgrade pip
RUN pip install setuptools

# where the code lives
WORKDIR $PYTHONPATH

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH "/root/.local/bin:$PATH"


COPY ../../poetry.lock pyproject.toml ./


RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-root --only main --no-interaction --no-ansi

COPY ../.. .
