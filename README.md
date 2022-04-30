# FHIR Project

This is project is developed as part of [EMIS Group](https://www.emishealth.com/) interview process.

To Run The Dockerized Django project clone or download the git repository and run following docker command.

    docker-compose up

Once the docker image is up go to [0.0.0.0:8000/admin](https://0.0.0.0:8000/admin). Then use the following login details
to log in.

    Username - user
    Passowrd - pwd

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

---
***The following of this README file will be updated with relevant documentation.***

Trello Link - https://trello.com/b/tfM1FR7D

## Key Decisions Made

    why python
    Django
    Library or reading json from scratch (fhir.resource Library)
    what FHIR recources are processing 

## Problems I encountered

## Problems I have still to address

## Testing

## Todo

- systems architecture
- database design

