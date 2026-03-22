FROM ubuntu:latest
LABEL authors="danielzhdanov"

ENTRYPOINT ["top", "-b"]