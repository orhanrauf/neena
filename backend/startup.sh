poetry export -f requirements.txt --output requirements.txt --without-hashes

python -m venv venv

source venv/bin/activate

pip install poetry 
pip install uvicorn 
pip install gunicorn


uvicorn --version

pip install -r requirements.txt


# poetry config virtualenvs.create false
# poetry install

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app