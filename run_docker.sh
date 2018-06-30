#!/usr/bin/env bash

echo Matando procesos viejos
docker-compose rm -fs

echo Creando containers nuevos
docker-compose up --build -d

echo Corriendo fixtures
docker exec app-backend bash -c 'cd core ; python manage.py db upgrade; python fixtures.py'
