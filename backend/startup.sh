python -m venv venv

source venv/bin/activate

pip install poetry 
pip install uvicorn 
pip install gunicorn


uvicorn --version

pip install -r requirements.txt

echo "========================================"
echo "Running the application"


uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --reload