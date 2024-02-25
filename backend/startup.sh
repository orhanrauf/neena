python -m venv venv

source venv/bin/activate

pip install poetry 
pip install uvicorn 
pip install gunicorn


uvicorn --version

pip install -r requirements.txt


gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000