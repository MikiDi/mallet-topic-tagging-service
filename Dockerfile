FROM lewg/mallet
MAINTAINER Michaël Dierick "michael@dierick.io"

ADD . /

ENV MEMORY=4g
ENV TRAIN_PATH=/data
ENV INPUT_PATH=/tmp/mallet-data/input-data
ENV OUTPUT_PATH=/tmp/mallet-data/input-data
# mu-python-template env vars
ENV APP_ENTRYPOINT web_mallet
ENV LOG_LEVEL info
ENV MU_SPARQL_ENDPOINT 'http://database:8890/sparql'
ENV MU_SPARQL_UPDATEPOINT 'http://database:8890/sparql'
ENV MU_APPLICATION_GRAPH 'http://mu.semte.ch/application'

RUN apt-get update && apt-get install -y \
    python3 \
    pip3
# mu-python-template stuff
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD ./mu-python-template /usr/src/app

RUN ln -s /app /usr/src/app/ext \
     && cd /usr/src/app \
     && pip3 install -r requirements.txt

ONBUILD ADD ./mu-python-template /app/
ONBUILD RUN cd /app/ \
    && pip3 install -r requirements.txt

EXPOSE 80

CMD python3 web.py
