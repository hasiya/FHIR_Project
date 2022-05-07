# FHIR Project

This project is developed as part of a technical assignment for a company that supplies software in various areas of
Healthcare. I was given some [FHIR](https://www.hl7.org/fhir/overview.html) data and the task was to transform these
FHIR messages into a more workable format preferably in a tabular format.

## The Git repo File structure

```markdown
.
├── Dockerfile --------------------- The Docker file
├── EMIS_FHIR_extract_data/ -------- The folder containing example data and the python file to read the FHIR files
│ ├── data/ ------------------------ Example FHIR JSON files
│ └── get_resources.py ------------- The initial python script that I wrote to understand FHIR data
├── FHIR_Project/ ------------------ The folder contains Django project files
├── README.md ---------------------- The Readme file
├── docker-compose.yaml ------------ The Docker Compose yaml file with PostgreSQL database service
├── fhir_db/ ----------------------- The folder contains Django app file
├── manage.py ---------------------- The manage.py file to run different Django commands
├── manage_db/ --------------------- The folder contains python scripts to manage Database
│ ├── __init__.py---
│ ├── create_admin_user.py --------- Python script to create a Django admin user
│ ├── db_functions.py -------------- The python file that contains functions to process FHIR JSON files, create Django admin user and Delete data in the FHIR database
│ ├── empty_db .py ----------------- Python script to delete data in the FHIR database
│ └── populate_db.py --------------- Python script to populate the FHIR database from Example FHIR JSON files
├── migrate_and_create_user.sh ----- The bash script to run Django 'migrate' command and create the Django admin user
└── requirements.txt --------------- The requirement file install python packages
```

Trello Link - https://trello.com/b/tfM1FR7D

## Key Decisions Made

### Python

The position I was applying was a Python developer, I decide it was appropriate to develop the solution in Python.

### Django

I used [Django](https://www.djangoproject.com/) web framework to develop the solution. Django is a high-level Python web
framework that allows you to develop complex web applications quickly without worrying about things like database
integration, user authentication, content administration etc. The reason for choosing Django to develop this solution
was the time frame of the technical assignment, and I didn't want think about database connections and writing SQL
queries as Django handles all that.

### Database - PostgreSQL

I am using a PostgreSQL database to store the process FHIR data. initially I was using a SQLite database to store the
FHIR
data as SQLite is the default database for Django projects. However, later I decided to change the database to
PostgreSQL, so I could get some experience on Django database configuration on PostgreSQL. As well as SQLite and
PostgreSQL Django officially supports MariaDB, MySQL and Oracle.

### Using a Library to handle FHIR data

In the start of the project I had two options for processing FHIR data files. First option is to read JSON file manually
and extract the data, the second option is to use a library to process FHIR JSON files and extract the FHIR data. I
decided to use a Python library called [FHIR Resources](https://pypi.org/project/fhir.resources/). This library allowed
me to create FHIR resource objects just by parsing the JSON string.

Following is an example of creating a FHIR resource object from a JSON string.

```python
from fhir.resources.organization import Organization

json_str = '''{
        "resourceType": "Organization",
        "id": "f001",
        "active": True,
        "name": "Acme Corporation",
        "address": [{"country": "Switzerland"}]     
    }'''
org = Organization.parse_raw(json_str)  ## Creates a Organization FHIR resource object.
```

## Run the dokcerized Django project and access the Django Admin site

To Run The Dockerized Django project clone or download the git repository and run following docker command.

    docker-compose up

Once the Docker image is up and Django server is running, you have to run the Django 'migrate' command to create
relevant Django database tables and create a Django admin user to access the Django Admin site. To do all this I have
created a bash script which will run the appropriate commands in the Docker container. Run the following command in a
separate terminal (if the Django server is running).

    ./migrate_and_create_user.sh    

Once the Docker image is up, the database migration is done and the Django Admin site user is created, go to
[http://0.0.0.0:8000](http://0.0.0.0:8000/). This page allows you to upload FHIR data files in JSON format and the
process the data in to the database. You can go to the Django Admin site
([http://0.0.0.0:8000/admin](http://0.0.0.0:8000/admin)) to view the processed FHIR data. Use the following login
details to access the Django Admin site.

    Username - user
    Passowrd - pwd
