#!/bin/bash

nvidia-docker run --rm -it \
	--workdir /home/jmpag/ --user $(id -u):$(id -g) \
	--name hloc \
	-v /gel/usr/jmpag11/code/:/home/jmpag/code/ \
	-v /gel/usr/jmpag11/dataset:/home/jmpag/dataset/ \
	-v /gel/usr/jmpag11/.ssh/id_ed25519:/home/jmpag/.ssh/id_ed25519 \
	-v /gel/usr/jmpag11/.gitconfig:/home/jmpag/.gitconfig \
	-p 8501:8501 \
	--shm-size=30G \
	jmpag11/hloc:v0.1 /bin/bash \