#!/bin/bash

test -z $1 && TAG="latest" || TAG="$1"

docker run \
--log-driver json-file \
--log-opt max-size=10m \
-v /dev/log:/dev/log \
-v /etc/localtime:/etc/localtime \
-v $HOME:/mnt/ \
-v $HOME/.ssh:/home/user/.ssh/ \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-h docker-centos7 \
--net host \
--name python-me-repls \
--rm -ti \
ipanema:5000/python-me-repls:$TAG
