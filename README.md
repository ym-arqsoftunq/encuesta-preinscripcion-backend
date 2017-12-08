# encuesta-preinscripcion-backend

> Un proyecto Flask

## Instalacion
Con virtualenv:

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

Levantar servidor Unicorn
``` bash
$ gunicorn --pythonpath core app:app

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
