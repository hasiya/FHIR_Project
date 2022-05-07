#!/bin/bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage_db/create_admin_user.py
