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

#### Crecimiento del tráfico temporal

Se realizan pruebas durante 15 minutos, llegando hasta los 800 usuarios simultáneos.

##### Tabla de transacciones
![Transacciones](/performance_tests/1_instancia_mediocpu/transacciones.png)
La cantidad de transacciones en 15 minutos llega a 9.589.

##### Gráfico de errores
![Errores](/performance_tests/1_instancia_mediocpu/error.png)
El porcentaje de errores en promedio es de 10.90%, llegando al 30% cuando hay 800 usuarios simultáneos.

#### Uso de recursos por contenedor
![Hosts](/performance_tests/1_instancia_mediocpu/hosts.png)
Se observa cómo la cantidad de CPU en promedio llega al 61%.

##### Gráfico tiempos de respuesta
![Linea](/performance_tests/1_instancia_mediocpu/linea.png)

##### Gráfico de requests por minuto (RPM)
![Linea](/performance_tests/1_instancia_mediocpu/rpm.png)
La cantidad de requests por minuto (RPM) llega a 533 en promedio.

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

#### Crecimiento del tráfico temporal

Se realizan pruebas durante 15 minutos, llegando hasta los 800 usuarios simultáneos.
3 instancias

##### Tabla de transacciones
![Transacciones](/performance_tests/1_instancia/Transacciones_1.png)
La cantidad de transacciones en 15 minutos es de 13.324 en total.

##### Gráfico de errores
![Errores](/performance_tests/1_instancia/Error_1.png)
El porcentaje de errores en promedio es de 8.89%, superando el 10% a partir de 300 usuarios y llegando a un 30% con 800 usuarios.
Esto muestra una mejora considerable con respecto a la prueba anterior.

#### Uso de recursos por contenedor
![Hosts](/performance_tests/1_instancia/Hosts_1.png)
Se puede observar cómo con un sólo contenedor, el uso de cpu es alto. Si bien en promedio parece normal (52%), teniendo en cuenta que la cantidad de usuarios es incremental, llegó al 96% gran parte del final de la prueba.

##### Gráfico tiempos de respuesta
![Linea](/performance_tests/1_instancia/Linea_1.png)

##### Gráfico de requests por minuto (RPM)
![Linea](/performance_tests/1_instancia/Rpm_1.png)
La cantidad de requests por minuto (RPM) es en promedio 784.
Esto muestra una mejora con respecto a la prueba anterior, de casi 250 requests por minuto.



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

#### Crecimiento del tráfico temporal

Se realizan pruebas durante 15 minutos, llegando hasta los 800 usuarios simultáneos.

##### Tabla de transacciones
![Transacciones](/performance_tests/3_instancias/Transacciones_3.png)
La cantidad de transacciones en 15 minutos llega a 20.085, casi 7mil transacciones más.

##### Gráfico de errores
![Errores](/performance_tests/3_instancias/Error_3.png)
El porcentaje de errores en promedio disminuye al 3.56%. Superando el 10% sólo cuando la cantidad de usuarios simultáneos es cercana a 800.

#### Uso de recursos por contenedor
![Hosts](/performance_tests/3_instancias/Hosts_3.png)
Se puede observar como Nginx divide la carga de forma equitativa. La cantidad de cpu en promedio disminuye considerablemente.

##### Gráfico tiempos de respuesta
![Linea](/performance_tests/3_instancias/Linea_3.png)

##### Gráfico de requests por minuto (RPM)
![Linea](/performance_tests/3_instancias/Rpm_3.png)
Se puede observar un crecimiento en la cantidad de requests por minuto (RPM) llegando a un promedio de 1.120 (casi 400 rpm más).
