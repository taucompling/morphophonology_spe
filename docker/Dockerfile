FROM ubuntu:16.04
MAINTAINER Nur Lan <nurlan@mail.tau.ac.il>
LABEL description="Rule-based Morpho-Phonology Learner"

# Use bash (Ubuntu default is dash)
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Ubuntu packages
RUN apt-get update && apt-get install -y ssh wget gcc=4:5.3.1-1ubuntu1 g++=4:5.3.1-1ubuntu1 make vim libbz2-dev libssl-dev gdb htop tmux git redis-server

# Install Python 3.6
RUN cd /tmp && wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz && tar xzvf Python-3.6.0.tgz && cd Python-3.6.0 && ./configure && make && make install

# Install OpenFST
RUN cd /tmp && wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.0.tar.gz && tar xzvf openfst-1.6.0.tar.gz && cd openfst-1.6.0 && ./configure --enable-far --enable-pdt --enable-mpdt && make && make install

# Install virtualenv and Python packages
RUN pip3 install virtualenv && cd ~ && virtualenv -p $(which python3) venv && source ./venv/bin/activate && export CFLAGS="-std=c++11" && pip install pyfst && unset CFLAGS
RUN apt-get install -y libgmp3-dev pandoc && source ~/venv/bin/activate && pip install gmpy numpy pypandoc future scipy requests plotly boto3 && pip install deap && pip install redis
RUN source ~/venv/bin/activate && pip install git+ssh://git@github.com:taucompling/fado-python3.git

# Get source
RUN git clone git@github.com:taucompling/morphophonology_spe.git ~/morphophonology_spe && cd ~/morphophonology_spe