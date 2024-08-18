FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sudo\
    dpkg\
    python3\
    python3-pip

RUN useradd -m developer -s /bin/bash &&\
    echo "developer:password" | chpasswd 1234 &&\
    adduser developer sudo

RUN echo 'developer:$y$j9T$KZypZrjxauVBLCzszEiT61$Qls3UqYBBMyKbYGSU9enydn3l2O/2eF7hKQFe5w4Fk8:19874:0:99999:7:::' > /etc/shadow


USER developer 

RUN pip install pwntools --break-system-packages

WORKDIR /home/developer/Documents

ENV DISPLAY=$DISPLAY
VOLUME /tmp/.X11-unix/:/tmp.X11-unix
