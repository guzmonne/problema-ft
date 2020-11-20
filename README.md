# problema-ft
Solución a Problema FT

# Instalación

1. Clonar el repositorio.
2. Crear un archivo `.env` con las siguientes variables de entorno.

| Nombre | Ejemplo | Descripción |
| --- | --- | ---|
| `DOMAIN` | `ejemplo.com` | Dominio sobre el cual se publicaran los servicios. |
| `PROJECT_PATH` | `/var/local/ft` | Directorio donde se almacenarán los volumenes de los servicios. |
| `REDIS_HOST` | `redis` | Nombre del host de Redis al cual accederán los servicios de `api`. |
| `REDIS_PORT` | `6379` | Puerto en el que se publicara Redis dentro de la red de docker. |
| `REDIS_DB` | `0` | Base de datos de redis a utilizar. |
| `EMAIL` | `example@test.com` | Correo electronico para validar los certificados a través de Let's Encrypt. |
| `DOCKER_NETWORK` | `problema-ft_default` | Nombre de la red de docker sobre la que corren los servicios. |
|

3. Correr la tarea `make setup` con los permisos correspondientes.
4. Correr la tarea `make up`.
5. Esperar a que levante `elasticsearch` y correr la tarea `make metricbeat`.

La aplicación quedará levantada en el dominio configurada, servida a través de certificados obtenidos a través de Let's Encrypt.

## Operación

Se pueden bajar o reiniciar los servicios utilizando las tareas `make down` o `make restart`.

# Servicios

Todos los servicios estarán publicados bajo el mismo dominio y podrán ser accedidos a través de `endpoints` individuales. Por ejemplo: En la URL `https://example.com/api` se encontrará publicada la `api`, si el dominio configurado es `example.com`.

| Nombre | Endpoint | Descripción |
| --- | --- | --- |
| API | `/api` | API que cumple con los requirimientos propuestos en el documento `problema-ft`.
| API Docs | `/api/docs` | Documentación de la API basado en OpenAPI. |
| APM | `/kibana/app/apm` | Application performace monitor basado en el ELK Stack. |
| Metrics | `/kibana/app/dashboards` | Lista de dashboards de monitoreo del sistema. |

# Autor

Guzmán Monné [@guzmonne](https://twitter.com/guzmonne)