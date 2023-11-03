#!/bin/sh

export $(grep -v '^#' .env | xargs -d '\n')
# tail -f /dev/null
# python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

