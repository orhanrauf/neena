pip install poetry uvicorn gunicorn

poetry install

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app