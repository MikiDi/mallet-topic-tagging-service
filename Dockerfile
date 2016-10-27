FROM lewg/mallet
MAINTAINER Michaël Dierick "michael@dierick.io"

RUN apt-get update && apt-get install -y \
    python3

ADD start.sh /
ADD setup-memory.sh /
ADD import-directory.sh /
ADD infer-topics.sh /

ENV MEMORY=4g
ENV TRAIN_PATH=/data
ENV INPUT_PATH=/tmp/mallet-data/input-data
ENV OUTPUT_PATH=/tmp/mallet-data/input-data
