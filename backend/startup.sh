#!/bin/bash

pip install -r requirements.txt
pip install uvicorn

echo "========================================"
echo "Running the application"


uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4