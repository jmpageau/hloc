FROM nvidia/cuda:11.5.0-cudnn8-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        sudo \
        locales \
        software-properties-common \
        build-essential \
        cmake \
        gdb \
        gfortran \
        wget \
        curl \
        ssh \
        rsync \
        keychain \
        git \
        git-lfs \
        zip \
        unzip \
        vim \
        imagemagick \
        ffmpeg \
        openexr \
        libopenexr-dev \
        python3 \
        python3-pip \
        python3-dev \
        python3-setuptools \
        cython \
        python-is-python3 \
        build-essentials  && \
        apt-get install -y wget && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*


RUN apt-get -y autoremove && apt-get -y clean

# Locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Python packages
RUN pip3 install --upgrade pip && pip3 install \
        numpy==1.22 \
        numba==0.56.0 \
        cupy-cuda116==10.6.0 \
        tensorflow-gpu==2.9.1 \
        tensorboardX==2.5.1 \
        torch==1.13.0 \
        scikit-learn==1.1.2 \
        scikit-image==0.19.3 \
        pandas==1.4.3 \
        matplotlib==3.5.3 \
        streamlit==1.12.0 \
        imageio==2.21.1 \
        imageio-ffmpeg==0.4.7 \
        opencv-python==4.6.0.66 \
        OpenEXR==1.3.8 \
        skylibs==0.7.0 \
        pycolmap==0.3.0 \
        tqdm==4.36.0 \
        kornia==0.6.8 \
        plotly==5.11.0 \
        scipy==1.9.3 \
        h5py==3.7.0 \
        gdown==4.5.3

RUN pip3 install \
        torch==1.13.0 \
        torchvision==0.14.0 \
        torchaudio==0.13.0 \
        --extra-index-url https://download.pytorch.org/whl/cu113

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# User setup
ARG username=jmpag
ARG passwd=dock
ARG uid
ARG gid
RUN useradd -ms /bin/bash $username
RUN echo $username:$passwd | chpasswd && usermod -aG sudo $username
RUN echo 'root:root' | chpasswd


EXPOSE 8501