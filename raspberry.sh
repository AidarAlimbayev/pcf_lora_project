#!/usr/bin/env bash 
set -Eeuo pipefail


apt update
apt -y upgrade
echo `python3 -V`
apt install -y python3-pip
echo `python3 -V`
echo 'The Python has loaded'
echo '###########################################################################################'
sleep 3

cd ~/Documents/
git clone https://github.com/AidarAlimbayev/pcf_lora_project.git
#cp pcf_lora_project/software/main/main_pcf_ver4.py /home/pi/
#cp pcf_lora_project/software/main/lib_pcf_ver4.py /home/pi/
cp pcf_lora_project/software/main/main_aid_ver3.py /home/pi/
cp pcf_lora_project/software/main/main_lib_ver3.py /home/pi/
cp pcf_lora_project/software/main/pcf.service /etc/systemd/system/
cp pcf_lora_project/software/main/99-serial-logger.rules /etc/udev/rules.d/



echo 'Project has loaded'
echo '###########################################################################################'
sleep 3

pip install serial          #import serial
pip install python-time     #import time
pip install sockets         #import socket
pip install jsonlib         # - Не уверен /import json 
pip install requests        #import requests
pip install pycopy-binascii #import binascii
pip install python-csv      #import csv
pip insatll regex           #import re
pip install logging         #import logging
pip install os-sys          #import os
pip install statistics      #import statistics

echo 'All libraries has loaded'
echo '###########################################################################################'
sleep 3


#cd "/dev"
#chmod 777 ttyUSB0
#chmpd 777 ttyASM0 



#merge git узнать