# FHIR Project

This project is developed as part of a technical assignment for a company that supplies software in various areas of
Healthcare. I was given some [FHIR](https://www.hl7.org/fhir/overview.html) data and the task was to transform these
FHIR messages into a more workable format preferably in a tabular format.

The Git repo File structure

```markdown
├── Dockerfile ------------------ The Docker file
├── EMIS_FHIR_extract_data/ ----- The folder containing example data and the python file to read the FHIR files
│ ├── data/ --------------------- Example FHIR json files
│ └── get_resources.py ---------- The initial python script that I wrote to understand FHIR data
├── FHIR_Project/ --------------- The folder contains Django project files.
├── README.md ------------------- The Readme file
├── db.sqlite3 ------------------ The SQLite database file
├── docker-compose.yaml --------- The Docker Compose yaml file.
├── fhir_db/ -------------------- The folder contains Django app file
├── manage.py ------------------- The manage.py file to run different Django commands
├── populate_db.py -------------- The python file populates the SQLite database with example FHIR json files in the 'EMIS_FHIR_extract_data/data/' folder
└── requirements.txt ------------ The requirement file install python packages 
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

### Database - SQLite

I am using a SQLite database to store the process FHIR data. The reason for choosing SQLite is that by default the
Django configuration uses SQLite. As well as SQLite Django officially supports PostgreSQL, MariaDB, MySQL and Oracle.

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

Once the Docker image is up go to [0.0.0.0:8000](https://0.0.0.0:8000/). This page allows you to upload FHIR data files
in JSON format and the process the data in to the database. You can go to the Django admin site
([0.0.0.0:8000/admin](https://0.0.0.0:8000/admin)) to view the processed FHIR data. Use the following login details to
access the Django Admin site.

    Username - user
    Passowrd - pwd
