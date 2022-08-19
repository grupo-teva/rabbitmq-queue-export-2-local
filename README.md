# _Scripts_ para exportar/importar mensajes de colas de **RabbitMQ**

¿Qué pasa cuando queremos probar un servicio o un demonio que consume colas de **RabbitMQ**? ¿De dónde sacamos los mensajes? Del mismo sitio que lo haría el demonio en producción: los trincaremos del _RabbitMQ_ de producción.

En verdad, en verdad os digo que esto no es más que una capa que _dockerifica_ este estupendo pograma: [rabbitmq-dump-queue](https://github.com/dubek/rabbitmq-dump-queue)

¯\\\_(ツ)_/¯

Si en la instalación donde se encuentra el RabbitMQ de producción no tenemos posibilidad de montar _Docker_, aún podremos usar el binario de `rabbitmq-dump-queue`, aunque, _EMHO_, es más fácil a día de hoy contar con _Docker_ que con _Go_.

## Dependencias ♻

Para poder utilizar esta vaina necesitamos tener instalado todo esto:

* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/)
* [pip](https://pypi.org/project/pip/)
* [pika](https://pypi.org/project/pika/)

La parte más intensa de la instalación es la de las dependencias de _Python_; en sistemas `Debian GNU/Linux` y derivados será algo así:

```bash
❯ apt install python3-pip
```

```bash
❯ pip install --user pika
Collecting pika
  Downloading pika-1.3.0-py3-none-any.whl (155 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.3/155.3 KB 1.9 MB/s eta 0:00:00
Installing collected packages: pika
Successfully installed pika-1.3.0
```

## ¿Cómo funciona esto? 🔧

Construimos la imagen de _Docker_ para el contenedor en el que instalaremos el programa `rabbitmq-dump-queue`:

```bash
❯ docker build -t rabbitmq-queue-export .
```

Creamos el contenedor:

```bash
❯ docker run -it -v $PWD/data:/data rabbitmq-queue-export
```

### Exportar mensajes

Con el programa `rabbitmq-dump-queue` extraemos los mensajes que necesitamos de la cola en la que están. Para ello tenemos dos opciones:

* Completamos toda la información necesaria en la línea de comandos:

```bash
❯ rabbitmq-dump-queue \
    -uri="amqp://<USER_NAME>:<USER_PASSWD>@<RABBIT_HOST>:<RABBIT_PORT>/" \
    -queue=<queue_name> \
    -max-messages=<MAX_MESSAGES> \
    -output-dir=<DATA_PATH>
```

* O, si la situación lo requiere, creamos un fichero de variables a partir de la plantilla _config.sh.dist_, y ejecutamos el _script_ de exportación `export-rabbitmq-queue`:

```bash
❯ cp config.sh.dist config.sh
❯ vi config.sh ← aquí introducimos los valores adecuados
[...]
❯ ./export-rabbitmq-queue
```

Las opciones de exportación empleadas en el _script_ son las que aparecen en la invocación directa del programa. Por su indudable interés, es recomendable echar un vistazo a dichas opciones de exportación, que pueden encontrarse en el [README](https://github.com/dubek/rabbitmq-dump-queue#readme) de su repo.

En cualquier caso, seremos testigos de la exportación; cuando termine, podremos cerrar el contenedor y comprobar el resultado:

```bash
❯ du -sh <DATA_PATH>/
272M <DATA_PATH>/
❯ l <DATA_PATH>
-rw-r--r-- 1 teva teva 284K ago 18 14:10 msg-0000
[...]
-rw-r--r-- 1 teva teva 320K ago 18 14:10 msg-1998
-rw-r--r-- 1 teva teva   79 ago 18 14:10 msg-1999
```

En este punto podremos comprimir el directorio de salida completo ─si no lo hemos hecho ya automágicamente porque hemos leído el _README_ del programa─, y transferir el fichero a nuestra máquina por el medio que más nos convenza.

### Levantar un RabbitMQ local

Ahora que tenemos los datos, montemos nuestro _RabbitMQ_ local:

```bash
❯ ./run-local-rabbitmq
94111048d29afe0fc942e83413c6d2b0637d28dc95f7c1d55b5f1a32ae4d92b3
```

```bash
❯ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                                                                                                                 NAMES
94111048d29a   rabbitmq:3-management       "docker-entrypoint.s…"   30 seconds ago   Up 29 seconds   4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, :::5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp, :::15672->15672/tcp   local-rabbitmq
```

La imagen para _RabbitMQ_ incluye el _plug-in_ `management`, así que si abrimos nuestro navegador web favorito podremos, por ejemplo, cargar la configuración del nodo original, o verificar el proceso de importación de los mensajes: `http://localhost:15672/`

### Importar los mensajes en el RabbitMQ local

Dependiendo de la naturaleza de los mensajes, tenemos dos _scripts_ de Python:

* Los mensajes son texto plano, por ejemplo, JSON.

```bash
❯ ./build-local-queue.py
```

* Los mensajes son binarios, por ejemplo, [protobuf](https://developers.google.com/protocol-buffers).

```bash
❯ ./build-local-binary-queue.py
```

Ambos _scripts_ utilizan una clase común para las operaciones de conexión, desconexión, envío y tal, definida en _rabbit.py_, y un mismo fichero de configuración, que se debe construir a partir de la plantilla _config.py.dist_

### Eliminar la cola para volver a empezar

Existe un último _script_ de Python que nos permite eliminar la cola de nuestro _RabbitMQ_ local para repetir la operación de importación, si fuera necesario:

```bash
❯ ./remove-local-queue.py
```

Este _script_ utiliza el nombre de la cola definido en _config.py_, aunque también admite un argumento, (¡Oh, sorpresa) el nombre de la cola:

```bash
❯ ./remove-local-queue.py <QUEUE_NAME>
```

## ¿Qué se puede mejorar? 📑

* _Dockerificar_ también _Python_ y sus dependencias.
