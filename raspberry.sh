#!/usr/bin/env bash 
set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

#Установка Git
apt-get install git


apt update
apt -y upgrade
echo `python3 -V`
apt install -y python3-pip
echo `python3 -V`
echo 'The Python has loaded'
echo '###########################################################################################'
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

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
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

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
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 


#cd "/dev"
#chmod +x ttyUSB0
#chmpd +x ttyASM0 



#merge git узнать