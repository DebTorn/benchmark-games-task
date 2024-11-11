#!/usr/bin/env bash
set -e

echo "Migrate Database"
if [[ $(poetry run python3 -m alembic heads) == $(poetry run python3 -m alembic current) ]]; then
    echo "No migrations to apply"
else
    poetry run python3 -m alembic upgrade head
fi

echo "Start Application"
poetry run python3 -m uvicorn src.main:app --host=0.0.0.0 --port=8000