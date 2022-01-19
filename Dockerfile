FROM python:3.9-buster

LABEL "com.multix.vendor"="Multix Tecnologia Ltda"
LABEL org.opencontainers.image.authors="joaquim.mattos@gmail.com"

LABEL version="1.0"
LABEL description="Eufrates is an experimental Python BPM engine"

# make sure all is updated
RUN apt-get -y update && apt-get upgrade -yu

COPY . /tmp/eufrates

RUN cd /tmp/eufrates && make wheel && pip install dist/eufrates*.whl

