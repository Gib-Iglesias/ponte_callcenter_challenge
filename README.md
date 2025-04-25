# Why this Project was Created? #

"""
This repository is the solution created for a code test with the following statement:
"You are leading the development of a call center simulation system that will efficiently manage the handling of a given number of tickets. The system must assign tickets to N agents in parallel and record both the time the ticket is assigned and the time it is completed in a CSV file."
"""

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
pip install -r requirements.txt (Windows)
pip3 install -r requirements.txt (Mac / Linux)

### Check List of Requirements Installed (Only IF needed):
pip freeze req.txt (Windows)
pip3 freeze req.txt (Mac / Linux)

### Apply Migrations
python manage.py makemigrations
python manage.py makemigrations [app_name] (Only IF needed)
python manage.py migrate

### To Runserver:
python manage.py runserver
python manage.py runserver [run in specific port: 0.0.0.0:8000]

### To Run Tests:
python manage.py test call_center


## AutoDocumentation with Swagger
You can check all the APIs created for the project and how to use it in
URLs: 'http://127.0.0.1:8000/api/schema/swagger-ui/' or 'http://localhost:8000/api/schema/swagger-ui/'
