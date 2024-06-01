#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
sudo apt update && sudo apt install sudo dpkg python3 python3-pip -y && sudo pip install pwntools --break-system-packages 
