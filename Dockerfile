FROM golang:latest

VOLUME ["/rabbit"]

RUN go install github.com/dubek/rabbitmq-dump-queue@latest

ENTRYPOINT ["/bin/bash"]
