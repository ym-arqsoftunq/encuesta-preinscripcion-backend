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
