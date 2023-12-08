pip install poetry 
pip install uvicorn 
pip install gunicorn


uvicorn --version

poetry install

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app