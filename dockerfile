# Creates a basic box for admin purposes

# Specify base
FROM ubuntu:20.04

# Specify where you want your workspace
ARG WORKDIR="/workspace"
WORKDIR $WORKDIR

# Update the box
RUN apt-get -y update

# Install basic tools
RUN apt-get install -y tmux python3-pip 

# Linux Tools
RUN apt-get install -y tmux
RUN apt-get install -y wget curl iputils-ping
RUN apt-get install -y zip unzip
RUN apt-get install -y jq

# Update the box (refresh apt-get)
RUN apt-get update -y

# Base Python
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN update-alternatives --install /usr/bin/python python $(which python3) 1
RUN pip3 install numpy tqdm
RUN pip3 install pyinstaller slack_sdk

# VS Code Server
# Note, not necessary, but significant time saver
RUN wget "https://update.code.visualstudio.com/latest/server-linux-x64/stable" -O /tmp/vscode-server-linux-x64.tar.gz \  
    && mkdir /tmp/vscode-server \  
    && tar --no-same-owner -zxvf /tmp/vscode-server-linux-x64.tar.gz -C /tmp/vscode-server --strip-components=1 \  
    && commit_id=$(cat /tmp/vscode-server/product.json | grep '"commit":' | sed -E 's/.*"([^"]+)".*/\1/') \  
    && mkdir -p ~/.vscode-server/bin/${commit_id} \  
    && cp -r /tmp/vscode-server/*  ~/.vscode-server/bin/${commit_id}/. 

# Update the box (refresh apt-get)
RUN apt-get update -y

# Install pytorch
RUN pip3 install torch torchvision torchaudio

# For tensorboard
#RUN pip3 install tensorboard tensorflow
# For tensorboard without tensorflow
RUN pip3 install tensorboardX

# Update the box (refresh apt-get)
RUN apt-get update -y

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Creates a non-root user with an explicit UID
ARG USER_NAME="jmpag"
ARG USER_ID=5678
ARG GROUP_ID=8765
RUN groupadd -g ${GROUP_ID} docker 
RUN useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash ${USER_NAME}
RUN echo "${USER_NAME}:jmpag" |  chpasswd 
USER $USER_ID:${GROUP_ID}

# Copy VS Code Server to USER
# Note, not necessary, but significant time saver
RUN commit_id=$(cat /tmp/vscode-server/product.json | grep '"commit":' | sed -E 's/.*"([^"]+)".*/\1/') \  
    && mkdir -p ~/.vscode-server/bin/${commit_id} \  
    && cp -r /tmp/vscode-server/*  ~/.vscode-server/bin/${commit_id}/.  