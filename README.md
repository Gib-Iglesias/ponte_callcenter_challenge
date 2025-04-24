# How to Run this Project #
## Python (Framework Django) ##

Create VENV:
python -m venv venv (Windows)
python3 -m venv venv (Mac / Linux)

Activate VENV:
source venv/bin/activate (Mac / Linux)
. venv\Scripts\activate (Windows)

Deactivate VENV:
deactivate (Inside venv)

Install Requirements
pip install -r requirements.txt (pip3 en Mac / Linux)

Check List of Requirements Installed
pip freeze requirements2.txt (pip3 en Mac / Linux)

Migrations
python manage.py makemigrations
python manage.py makemigrations [app_name] (si solo se requiere ejecutar un cambio de una sola app y no de todo el repo)
python manage.py migrate

Runserver
python manage.py runserver
python manage.py runserver [run in specific port: 0.0.0.0:8000]

To Run Tests
python manage.py test