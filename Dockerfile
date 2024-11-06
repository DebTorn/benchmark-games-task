FROM python:3.12.6-slim

ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

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
        pkg-config

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY --chown=www-data:www-data . .

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

CMD ./docker-entrypoint.sh