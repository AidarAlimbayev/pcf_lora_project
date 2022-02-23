#!/usr/bin/env bash 
set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)


apt update                          #Проверка обновлении
apt -y upgrade                      #Установка обновлении 
apt-get dist-upgrade                #Обновление raspbian до последней версии

#Установка Git
apt-get install git

#Установка VNC
apt-get install tightvncserver      

#Установка TeamViewer
#wget https://www.teamviewer.com/ru/%d1%81%d0%ba%d0%b0%d1%87%d0%b0%d1%82%d1%8c/raspberry-pi/teamviewer_15.26.4_armhf.deb
#dpkg -i teamviewer-host_armhf.deb
#apt --fix-broken install           

#Установка Python
echo `python3 -V`
apt install python2
apt install -y python3-pip
echo `python3 -V`
echo 'The Python has loaded'
echo '###########################################################################################'
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

#Установка проекта
#cd ~/Documents/
#git clone git@github.com:AidarAlimbayev/pcf_lora_project.git
#cp software/main/main_pcf_ver4.py /home/pi/
#cp software/main/lib_pcf_ver4.py /home/pi/
##cp pcf_lora_project/software/main/main_aid_ver3.py /home/pi/
##cp pcf_lora_project/software/main/main_lib_ver3.py /home/pi/
#cp software/main/pcf.service /etc/systemd/system/
#cp software/main/99-serial-logger.rules /etc/udev/rules.d/

# echo 'Project has loaded'
# echo '###########################################################################################'
# for ((i = 1; i <= 3; i++))
# do
# echo "...$i"
# sleep 1
# done 

pip install serial          #import serial
pip install python-time     #import time
pip install sockets         #import socket
#pip install jsonlib         # - Не уверен /import json 
#pip install requests        #import requests
#pip install pycopy-binascii #import binascii
pip install python-csv      #import csv
pip insatll regex           #import re
pip install logging         #import logging
#pip install os-sys          #import os
pip install statistics      #import statistics

echo 'All libraries has loaded'
echo '###########################################################################################'
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

#Установка Arduino IDE. *Примечание, перед установкой соединить с raspberry

mkdir ${HOME}/arduino
cd ${HOME}/arduino/
wget https://downloads.arduino.cc/arduino-1.8.15-linux64.tar.xz
tar -xvf ./arduino-1.8.15-linux64.tar.xz
cd ${HOME}/arduino/arduino-1.8.15/
./install.sh
if [ -f /dev/ttyASM* ]
then 
    chmod 777 ttyASM*
elif [ -f /dev/ttyUSB* ]
then
    chmod 777 ttyUSB*
else    
    echo "Подключитесь к Arduino"
    sleep 3
fi





