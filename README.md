# encuesta-preinscripcion-backend

> Un proyecto Flask

## Build con Docker

``` bash
# Instalar docker
$ sudo apt-get install docker.io
# Instalar docker-compose
$ sudo apt install docker-compose
# Instanciar el contenedor
$ sudo docker-compose build
# Correr el contenedor
$ sudo docker-compose up -d
```

## Instalacion con virtualenv

``` bash
# Instalar virtualenv (en Ubuntu)
$ sudo apt-get install python-virtualenv
# Clonar proyecto
$ git clone https://github.com/ym-arqsoftunq/encuesta-preinscripcion-backend.git
# Crear entorno
$ cd encuesta-preinscripcion-backend
$ virtualenv venv
# Activar entorno
$ . venv/bin/activate
# instalar dependencias
$ pip install -r requirements.txt
```

Levantar servidor Unicorn (asi se ejecuta en Heroku) en localhost:8000
``` bash
$ gunicorn --pythonpath core app:app

```

O levantar servidor de flask en localhost:5000
``` bash
$ FLASK_APP=core/app.py flask run

```
Para modo debug (ver errores en navegador y consola), antes de levantar el server con flask run, ejecutar
``` bash
$ export FLASK_DEBUG=1
```

Tests

``` bash
# run all tests
$ pytest
```

Desactivar virtualenv

``` bash
$ deactivate
```

### Persistencia
Se usa Postgres para poder deployar en heroku

``` bash
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib
```

Por defecto, la instalación nos crea el usuario postgres
``` bash
$ sudo -i -u postgres
```

Una vez instalado, vamos a entrar a la consola de psql
``` bash
$ psql
```

Una vez dentro, vamos a crear la base
``` bash
create database encuestas
```

Ya tenemos la Base de Datos, ahora hay que configurar nuestro proyecto.
En app.py
``` bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://localhost/encuestas'
```

El siguiente paso es crear el esquema de la base de datos y cargar los fixtures.
Debemos estar sobre el directorio core del proyecto
``` bash
$ python manage.py db upgrade
$ python fixtures.py
```

Si al ejecutar "python manage.py db upgrade" nos tira error por falta de contraseña, ponerle una al usuario postgres
``` bash
$ sudo -i -u postgres
$ psql
$ alter user postgres password 'una_password';
```
Y luego de poner la contraseña modificar la linea de app.py
``` bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:una_password@localhost:5432/encuestas'
```

#### Persistencia con Docker
Poner IP de la maquina (no localhost) en core/config.py
Una vez levantado el contenedor docker (ejecutado los pasos de "Build con Docker") ejecutar
``` bash
# Entrar al contenedor postgres
$ sudo docker exec -it postgres psql -U postgres
# Creo base de datos
$ CREATE DATABASE encuestas;
# Salgo del contenedor postgres
$ \q
# Entrar al contenedor de nuestra app
$ sudo docker exec -it app-backend bash
# Cargo la base de datos
$ cd core
$ python manage.py db upgrade
$ python fixtures.py
# Salgo del contenedor
$ exit
```
Esto hay que hacerlo solo la primera vez. Luego la base de datos (y los datos) se guardan en nuestra maquina y con $docker-compose up ya tenemos la app andando

### Swagger UI

Con la app levantada dirigirse a http://localhost:5000/api/spec.html
