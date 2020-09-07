#!/usr/bin/env bash
echo 'make migrations'
python manage.py makemigrations
echo 'migrate '${MANAGER_DB_SERVICE_NAME}
python manage.py migrate --database ${MANAGER_DB_SERVICE_NAME}
echo 'migrate '${ENGINE_DB_SERVICE_NAME}
python manage.py migrate --database ${ENGINE_DB_SERVICE_NAME}
