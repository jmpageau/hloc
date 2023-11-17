#!/bin/bash

docker build -f DockerfileLinux -t jmpag11/hloc:v0.1 \
	--build-arg uid=$(id -u) --build-arg gid=$(id -g) .