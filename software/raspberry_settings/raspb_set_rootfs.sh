#!/usr/bin/env bash                                                                       
set -Eeuo pipefail

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/ssh /media/maxat/boot1
chmod +x /media/maxat/boot1/ssh
echo `ls -l` /media/maxat/boot1/ssh
sleep 1
echo "1#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/wpa_supplicant.conf /media/maxat/boot1
chmod +x /media/maxat/boot1/wpa_supplicant.conf
echo `ls -l` /media/maxat/boot1/wpa_supplicant.conf
sleep 1
echo "2#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/main_pcf_ver4.py /media/maxat/rootfs/home/pi
chmod 777 /media/maxat/rootfs/home/pi/main_pcf_ver4.py
echo `ls -l` /media/maxat/rootfs/home/pi/main_pcf_ver4.py
sleep 1
echo "3#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/lib_pcf_ver4.py /media/maxat/rootfs/home/pi
chmod 777 /media/maxat/rootfs/home/pi/lib_pcf_ver4.py
echo `ls -l` /media/maxat/rootfs/home/pi/lib_pcf_ver4.py
sleep 1
echo "4#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/pcf.service /media/maxat/rootfs/etc/systemd/system
chmod 777 /media/maxat/rootfs/etc/systemd/system/pcf.service
echo `ls -l` media/maxat/rootfs/etc/systemd/system/pcf.service
sleep 1
echo "5#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/99-serial-logger.rules /media/maxat/rootfs/etc/udev/rules.d
chmod 777 /media/maxat/rootfs/etc/udev/rules.d/99-serial-logger.rules
echo `ls -l` /media/maxat/rootfs/etc/udev/rules.d/99-serial-logger.rules
sleep 1
echo "6#############"

chmod 777 /media/maxat/rootfs/etc/dhcpcd.conf
cat /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/dhcpcd.conf > /media/maxat/rootfs/etc/dhcpcd.conf
chmod 777 /media/maxat/rootfs/etc/dhcpcd.conf
echo "7###########"
cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/raspberry.sh /media/maxat/rootfs/home
echo "8###########"


