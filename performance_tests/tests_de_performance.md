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

#### Límites de la aplicación

Con 100 usuarios concurrentes la aplicación, si bien no se cae, funciona con tiempos no aceptables y con un porcentaje de error considerablemente alto, 17%.

Con 50 usuarios los tiempos de respuesta no son buenos pero el porcentaje de error se mantiene en cero. Así que podriamos concluir que ese es el límite de la aplicación en la configuración inicial de virtualización.

![Grafico de tiempo de respuesta](/performance_tests/ResponseTimeGraph1.png)

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

El total del test arroja un porcentaje de error de 1.68% y un tiempo promedio de respuesta de 9 segundos en un total de 2263 requests.

#### Límites de la aplicación

Con 100 hilos la aplicación no reportó errores y los tiempos de respuesta no fueron tan malos (tampoco pueden considerarse buenos). Por otro lado, con 150 hilos, aunque el porcentaje de error se mantuvo en cero, los tiempos de respuesta se duplicaron llegando a 12 segundos. Lo que es muy lento para una aplicación web. Por lo tanto podemos concluir que el límite de la aplicación con el crecimiento vertical aplicado es de 100 usuarios concurrentes.

![Grafico de tiempo de respuesta](/performance_tests/ResponseTimeGraph2.png)

### Agregamos dos instancias de docker con balanceo de carga. Crecimiento horizontal.

#### Parámetros de docker-compose.yml en las 3 instancias de la aplicación

``` bash
    # un cpu como maximo
    cpu_quota: 100000
    # 512 MB como maximo
    mem_limit: 512m
```

#### Pruebas con JMeter 3

En comparación con las "Pruebas con JMeter 2" se ve una gran mejora en cantidad de requests servidos y en tiempos de respuesta. Sin embargo también hay un incremento considerable en el procentaje de error que llamativamente ya puede verse en el primer minuto del test. Un dato importante es que todos los errores son del mismo request, el POST de la encuesta.

Minuto 1. 50 hilos. 450 Requests. El tiempo promedio de respuesta es de 778 ms y el porcentaje de error es de 2.22%.

Minuto 2. 100 hilos. 824 Requests. El tiempo promedio de respuesta es de 1693 ms y el porcentaje de error es de 2.55%.

Minuto 3. 150 hilos. 1066 Requests. El tiempo promedio de respuesta es de 2617 ms y el porcentaje de error es de 3.38%.

Minuto 4. 200 hilos. 1284 Requests. El tiempo promedio de respuesta es de 3814 ms y el porcentaje de error es de 4.44%.

El total del test arroja un porcentaje de error de 3.42% y un tiempo promedio de respuesta de 2.5 segundos en un total de 3624 requests.

#### Límites de la aplicación

Con 200 hilos concurrentes los tiempos de respuesta de la aplicación fueron relativamente buenos. Menos de 4 segundos en promedio. Pero el porcentaje de error en el submit de la encuesta es bastante alto, poco más de 14%. Todo indica que mejorando el proceso de submit de la encuesta, para reducir errores, los ĺímites de la aplicación, con esta configuración, son más altos.

![Grafico de tiempo de respuesta](/performance_tests/ResponseTimeGraph3.png)