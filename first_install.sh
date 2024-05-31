#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt update && apt install sudo dpkg python3 python3-pip -y && pip install pwntools --break-system-packages
python3 ~/documents/install.py
