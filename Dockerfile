FROM ubuntu:latest

ENV DISPLAY=$DISPLAY

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    sudo\
    dpkg\
    python3\
    python3-pip


VOLUME /tmp/.X11-unix/:/tmp.X11-unix

WORKDIR /root/Documents

VOLUME /home/angel/Documents/Proyect:/root/Documents


