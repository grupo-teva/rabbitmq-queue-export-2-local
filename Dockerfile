FROM golang:latest

VOLUME ["/data"]

RUN go install github.com/dubek/rabbitmq-dump-queue@latest

ENTRYPOINT ["/bin/bash"]
