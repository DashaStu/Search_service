#!/bin/bash
set -e

sleep 5


python -m scripts.import_data

exec uvicorn app.main:app --host 0.0.0.0 --port 8085 --reload