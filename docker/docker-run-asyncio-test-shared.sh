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
--name asyncio-test \
--rm -ti \
-v $HOME/my_work/srce/git.asyncio-test/asyncio-test:/home/user/asyncio-test-source \
ipanema:5000/asyncio-test:$TAG
