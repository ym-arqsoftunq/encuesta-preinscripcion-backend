### Configuración inicial de virtualización

#### Parámetros de docker-compose.yml

``` bash
    # medio cpu como maximo
    cpu_quota: 50000
    # 256 MB como maximo
    mem_limit: 256m
```

#### Pruebas con JMeter 1

Test de 4 minutos.

El primer minuto con 50 hilos haciendo requests. Si bien las respuestas no fueron demasiado rápidas, la aplicación se mantuvo estable. No hubo ningún error. Todos los requests fueron exitosos. 200 GET se respondieron en promedio en 3.5 segundos. El POST de la encuesta, que es el request más pesado de la aplicación, demoró en promedio 10 segundos, de un total de 100 requests.

En el segundo minuto se agregan 50 usuarios. La performance de la aplicación se ve muy perjudicada. El porcentaje de error es de 11% y el tiempo promedio de respuesta es de 17 segundos.

En el tercer minuto se agregan otros 50 usuarios. En total son 150. El porcentaje de errores sube a 33% y el tiempo promedio de respuesta es de 23 segundos.

En el cuarto minuto se agregan otros 50 hilos llegando a 200 concurrentes. El porcentaje de error es de 92% y y el tiempo promedio de respuesta es de 29 segundos.

El total del test arroja un porcentaje de error de 38% y un tiempo promedio de respuesta de 20 segundos.

![Grafico de tiempo de respuesta](/ResponseTimeGraph1.png)

### Agregamos más recursos a la aplicación. Crecimiento vertical.

Duplicamos los recursos de cpu y memoria en el contenedor de Docker.

#### Parámetros de docker-compose.yml

``` bash
    # un cpu como maximo
    cpu_quota: 100000
    # 512 MB como maximo
    mem_limit: 512m
```

#### Pruebas con JMeter 2

Las mejoras son notables con respecto al test anterior.

Minuto 1. 50 hilos. 385 Requests. El tiempo promedio de respuesta es de 1838 ms y el porcentaje de error es de 0%.

Minuto 2. 100 hilos. 616 Requests. El tiempo promedio de respuesta es de 5061 ms y el porcentaje de error es de 0%.

Minuto 3. 150 hilos. 556 Requests. Llamativamente se realizan menos requests que en el minuto 2. El tiempo promedio de respuesta es de 12202 ms y el porcentaje de error es de 0%.

Minuto 4. 200 hilos. 706 Requests. El tiempo promedio de respuesta es de 14173 ms y el porcentaje de error es de 5.38%. El porcentaje de error más alto estuvo en el POST de la encuesta donde fue de 13% y a su vez ese request tuvo el tiempo de respuesta mayor con un promedio de 22353 ms.

![Grafico de tiempo de respuesta](/ResponseTimeGraph2.png)