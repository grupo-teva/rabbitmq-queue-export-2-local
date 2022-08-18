#!/bin/bash

RABBIT_NAME='local-rabbitmq'

docker rm $RABBIT_NAME

docker run -d \
  --hostname $RABBIT_NAME \
  --name $RABBIT_NAME \
  -p 5672:5672 \
  -p 15672:15672 \
  -v $PWD/$RABBIT_NAME-mnesia:/var/lib/rabbitmq/mnesia/rabbit@$RABBIT_NAME \
  rabbitmq:3-management
