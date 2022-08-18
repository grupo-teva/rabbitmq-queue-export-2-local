# _Scripts_ para exportar/importar mensajes de colas de **RabbitMQ**

¿Qué pasa cuando queremos probar un servicio o un demonio que consume colas de **RabbitMQ**? ¿De dónde sacamos los mensajes? Del mismo sitio que lo haría el demonio en producción: los trincaremos del 

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

Extraemos los mensajes que necesitamos de la cola en la que están, completando toda la información necesaria:

```bash
❯ rabbitmq-dump-queue \
    -uri="amqp://<user>:<pass>@<url>:<port>/" \
    -queue=<queue_name> \
    -max-messages=2000 \
    -output-dir=/data
```

Seremos testigos de la exportación, y, cuando termine, podremos cerrar el contenedor y comprobar el resultado:

```bash
❯ du -sh data/
272M data/
❯ l data
-rw-r--r-- 1 teva teva 284K ago 18 14:10 msg-0000
[...]
-rw-r--r-- 1 teva teva 320K ago 18 14:10 msg-1998
-rw-r--r-- 1 teva teva   79 ago 18 14:10 msg-1999
```

Por su indudable interés, es recomendable echar un vistazo a las opciones de exportación de mensajes del programa, que pueden encontrarse en el [README](https://github.com/dubek/rabbitmq-dump-queue#readme) de su repo.

En este punto podremos comprimir el directorio `data` completo ─si no lo hemos hecho ya automágicamente─, y transferir el fichero a nuestra máquina por el medio que más nos convenza. Esto es, tenemos los datos, montemos nuestro _RabbitMQ_ local: 

```bash
❯ ./run-local-rabbitmq.sh
94111048d29afe0fc942e83413c6d2b0637d28dc95f7c1d55b5f1a32ae4d92b3
```

```bash
❯ docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                                                                                                                 NAMES
94111048d29a   rabbitmq:3-management       "docker-entrypoint.s…"   30 seconds ago   Up 29 seconds   4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, :::5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp, :::15672->15672/tcp   local-rabbitmq
```

La imagen para _RabbitMQ_ incluye el _plug-in_ `management`, así que si abrimos nuestro navegador web favorito podremos, por ejemplo, cargar la configuración del nodo original, u observar el proceso de importación de los mensajes: `http://localhost:15672/`

Por último, importamos los mensajes en la cola:

```bash
❯ ./scripts/build-local-queue.py
```

TODO: Poner más info en este punto.

## ¿Qué se puede mejorar? 📑

* Crear ficheros de variables de entorno para poder emplear los mismos _scripts_ en instalaciones distintas.
* Invocar también con variables al programa `rabbitmq-dump-queue`
* _Dockerificar_ también _Python_ y sus dependencias.
