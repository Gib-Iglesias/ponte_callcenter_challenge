# How to Run this Project #
## Python (Framework Django) ##

### Create VENV:
python -m venv venv (Windows)
python3 -m venv venv (Mac / Linux)

### Activate VENV:
source venv/bin/activate (Mac / Linux)
. venv\Scripts\activate (Windows)

### Deactivate VENV (Only IF needed):
deactivate (Inside venv)

### Install Requirements:
pip install -r requirements.txt (pip3 en Mac / Linux)

### Check List of Requirements Installed (Only IF needed):
pip freeze req.txt (pip3 en Mac / Linux)

### Apply Migrations
python manage.py makemigrations
python manage.py makemigrations [app_name] (Only IF needed)
python manage.py migrate

### To Runserver:
python manage.py runserver
python manage.py runserver [run in specific port: 0.0.0.0:8000]

### To Run Tests:
python manage.py test

## AutoDocumentation with Swagger
You can check all the APIs created for the project and how to use it
URLs: 'http://127.0.0.1:8000/api/schema/swagger-ui/' or 'http://localhost:8000/api/schema/swagger-ui/'
