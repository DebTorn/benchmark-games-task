FROM python:3.12.6-slim

ARG UID=1000
ARG GID=1000
ARG APP_TYPE=dev  # dev or prod

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN groupmod -g $GID www-data && usermod -o -u $UID www-data

RUN apt-get update && \ 
    apt-get install -y \ 
        zip \ 
        unzip \
        git \
        pkg-config \
        python3-dev \
        build-essential \
        default-libmysqlclient-dev \
        build-essential \
        pipx \
        pkg-config \
        curl && \
    apt-get clean

RUN pip install --upgrade pip && \
    pip install pipx && \
    python3 -m pipx ensurepath

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY --chown=www-data:www-data ./poetry.lock ./pyproject.toml /app/

RUN poetry install $(test "$APP_TYPE" = prod && echo "--only=main") --no-interaction --no-ansi

COPY --chown=www-data:www-data . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

CMD ./docker-entrypoint.sh