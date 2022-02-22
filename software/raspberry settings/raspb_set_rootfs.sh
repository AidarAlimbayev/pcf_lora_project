#!/usr/bin/env bash                                                                       
set -Eeuo pipefail

cp ~/.Projects/.Agrarka/pcf_lora_project/software/raspberry settings/ssh /media/maxat/boot
chmod +x /media/maxat/boot/ssh
echo `ls -l` /media/maxat/boot/ssh
sleep 1
echo "#############"

cp ~/.Projects/.Agrarka/pcf_lora_project/software/raspberry settings/wpa_supplicant.conf /media/maxat/boot
chmod +x /media/maxat/boot/wpa_supplicant.conf
echo `ls -l` /media/maxat/boot/wpa_supplicant.conf
sleep 1
echo "#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/main_pcf_ver4.py /media/maxat/rootfs/home/pi
chmod +x /media/maxat/rootfs/home/pi/main_pcf_ver4.py
echo `ls -l` /media/maxat/rootfs/home/pi/main_pcf_ver4.py
sleep 1
echo "#############"

cp /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/main/lib_pcf_ver4.py /media/maxat/rootfs/home/pi
chmod +x /media/maxat/rootfs/home/pi/lib_pcf_ver4.py
echo `ls -l` /media/maxat/rootfs/home/pi/lib_pcf_ver4.py
sleep 1
echo "#############"

cp ~/.Projects/.Agrarka/pcf_lora_project/software/main/pcf.service media/maxat/rootfs/etc/systemd/system
chmod +x media/maxat/rootfs/etc/systemd/system/pcf.service
echo `ls -l` media/maxat/rootfs/etc/systemd/system/pcf.service
sleep 1
echo "#############"

cp ~/.Projects/.Agrarka/pcf_lora_project/software/main/99-serial-logger.rules /media/maxat/rootfs/etc/udev/rules.d
chmod +x /media/maxat/rootfs/etc/udev/rules.d/99-serial-logger.rules
echo `ls -l` /media/maxat/rootfs/etc/udev/rules.d/99-serial-logger.rules
sleep 1
echo "#############"

chmod 777 /media/maxat/rootfs/etc/dhcpcd.conf
cat /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry\ settings/dhcpcd.conf > /media/maxat/rootfs/etc/dhcpcd.conf
chmod +x /media/maxat/rootfs/etc/dhcpcd.conf

cp /media/maxat/rootfs/home


