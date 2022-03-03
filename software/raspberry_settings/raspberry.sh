#!/usr/bin/env bash 
set -Eeuo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
echo "Введите пароль для системы Raspbian."
echo "Введите пароль: 321" 

apt update                          #Проверка обновлении
apt -y upgrade                      #Установка обновлении 
apt-get dist-upgrade                #Обновление raspbian до последней версии

#Внешний ip адрес
wget -qO- eth0.me >> myip.txt

#Установка Git
apt-get install git

#Локали 
# apt-get install locales
# nano /etc/environment >> LANG="ru_RU.UTF-8"
# nano /etc/locale.gen >> ru_RU.UTF-8 UTF-8
# locale-gen #Чтобы проверить ввести `locale -a`. На выходе должно быть POSIX en_US.utf8 ru_RU 

#Установка Python
echo `python3 -V`
apt install python2
apt install -y python3-pip
echo `python3 -V`
echo 'The Python has loaded'
echo '###################'
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

mkdir /home/pi/update
cd /home/pi/update
git clone https://github.com:pcfkazatu/pcf_kazatu_project.git

#Установка проекта
cd /home/pi/Documents/
git clone https://github.com/AidarAlimbayev/pcf_lora_project.git
#cp software/main/main_pcf_ver4.py /home/pi/
#chmod +x /home/pi/main_pcf_ver4.py
#cp software/main/lib_pcf_ver4.py /home/pi/
#chmod +x /home/pi/lib_pcf_ver4.py
##cp pcf_lora_project/software/main/main_aid_ver3.py /home/pi/
##cp pcf_lora_project/software/main/main_lib_ver3.py /home/pi/
#cp software/main/pcf.service /etc/systemd/system/
#chmod +x /etc/systemd/system/pcf.service
#cp software/main/99-serial-logger.rules /etc/udev/rules.d/
#chmod +x /etc/udev/rules.d/99-serial-logger.rules

# echo 'Project has loaded'
# echo '####################'
# for ((i = 1; i <= 3; i++))
# do
# echo "...$i"
# sleep 1
# done 

#Установка библиотек для python
#pip install os-sys          #import os
#pip install jsonlib         # - Не уверен /import json 
#pip install requests        #import requests
#pip install pycopy-binascii #import binascii
pip install serial          #import serial
pip install python-time     #import time
pip install sockets         #import socket
pip install python-csv      #import csv
pip install regex           #import re
pip3 install firmata
pip install httplib2 --upgrade
#pip install logging         #import logging
#pip install statistics      #import statistics
echo 'All libraries has loaded'
echo '####################'
for ((i = 1; i <= 3; i++))
do
echo "...$i"
sleep 1
done 

#Установка Arduino IDE. *Примечание, перед установкой соединить с raspberry
mkdir /home/pi/arduino
cd /home/pi/arduino/
wget https://downloads.arduino.cc/arduino-1.8.19-linuxarm.tar.xz
tar -xf arduino-1.8.19-linuxarm.tar.xz
sudo mv arduino-1.8.19 /opt
sudo /opt/arduino-1.8.19/install.sh

#Сначала проверяем подключен ли arduino 
TTYACM0=$(find /dev -name ttyACM0)
if test -z $TTYACM0; then
	echo "Arduino not found..."
    sleep 3
	exit
else
	echo "Arduino connected!"
fi

# Проверяем и подключаем user-a к подгруппе dialout
WHOAMI=$(whoami)
if [ $WHOAMI == "root" ]; then
	
	exit
else
	UGROUPS=$(groups $WHOAMI | grep -Eo "(dialout|tty)")
	if [[ $UGROUPS != *"dialout"* ]]; then
	    usermod -aG dialout $WHOAMI
	else
		echo "$WHOAMI already on dialout group"
	fi
	if [[ $UGROUPS != *"tty"* ]]; then
		usermod -aG dialout $WHOAMI
	else
		echo "$WHOAMI already on tty group"
	fi
fi

#Установка VNC
apt-get install realvnc-vnc-server
dpkg --add-architecture armhf && sudo apt update
apt install libx11-6
wget https://www.realvnc.com.download/file/vnc.files/VNC-Server-6.7.2-Linux-ARM.deb
systemctl start vncserver-x11-serviced-service
systemctl enable vncserver-x11-serviced.service
vnclicensewiz
echo "VNC done"

#Установка TeamViewer
cd /home/pi/Downloads/
wget https://download.teamviewer.com/download/linux/teamviewer-host_armhf.deb
dpkg -i teamviewer-host_armhf.deb || true
apt --fix-broken install  
#teamviewer passwd californicatioN 
# cd ${HOME}/Desktop
echo "#########" >> teamviewer_info.txt
teamviewer info >> teamviewer_info.txt
echo "TeamViewer done"

chmod a+rw /dev/ttyACM0
udevadm trigger
echo "All Done!"

raspi-config

#update-locale LC_ALL=ru_RU.UTF-8 LANG=ru_RU.UTF-8 LANGUAGE=ru_RU.UTF-8
