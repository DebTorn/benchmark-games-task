#!/usr/bin/env bash
set -e

echo "Migrate Database"
if [[ $(python3 -m alembic heads) == $(python3 -m alembic current) ]]; then
    echo "No migrations to apply"
else
    python3 -m alembic upgrade head
fi

echo "Start Application"
python3 -m uvicorn src.main:app --host=0.0.0.0 --port=8000