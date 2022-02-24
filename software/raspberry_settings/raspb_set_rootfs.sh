#!/usr/bin/env bash                                                                       
set -Eeuo pipefail
SCRIPT_PATH=$( cd $(dirname $0)/../ ; pwd )

cp ${SCRIPT_PATH}/raspberry_settings/ssh ${HOME}/boot1
chmod +x ${HOME}/boot1/ssh
echo `ls -l` ${HOME}/boot1/ssh
sleep 1
echo "1#############"

cp ${SCRIPT_PATH}/raspberry_settings/wpa_supplicant.conf ${HOME}/boot1
chmod +x ${HOME}/boot1/wpa_supplicant.conf
echo `ls -l` ${HOME}/boot1/wpa_supplicant.conf
sleep 1
echo "2#############"

cp ${SCRIPT_PATH}/main/main_pcf_ver4.py ${HOME}/rootfs/home/pi
chmod 777 ${HOME}/rootfs/home/pi/main_pcf_ver4.py
echo `ls -l` ${HOME}/rootfs/home/pi/main_pcf_ver4.py
sleep 1
echo "3#############"

cp ${SCRIPT_PATH}/main/lib_pcf_ver4.py ${HOME}/rootfs/home/pi
chmod 777 ${HOME}/rootfs/home/pi/lib_pcf_ver4.py
echo `ls -l` ${HOME}/rootfs/home/pi/lib_pcf_ver4.py
sleep 1
echo "4#############"

cp ${SCRIPT_PATH}/main/pcf.service ${HOME}/rootfs/etc/systemd/system
chmod 777 ${HOME}/rootfs/etc/systemd/system/pcf.service
echo `ls -l` media/maxat/rootfs/etc/systemd/system/pcf.service
sleep 1
echo "5#############"

cp ${SCRIPT_PATH}/main/99-serial-logger.rules ${HOME}/rootfs/etc/udev/rules.d
chmod 777 ${HOME}/rootfs/etc/udev/rules.d/99-serial-logger.rules
echo `ls -l` ${HOME}/rootfs/etc/udev/rules.d/99-serial-logger.rules
sleep 1
echo "6#############"

chmod 777 ${HOME}/rootfs/etc/dhcpcd.conf
cat ${SCRIPT_PATH}/raspberry_settings/dhcpcd.conf > ${HOME}/rootfs/etc/dhcpcd.conf
chmod 777 ${HOME}/rootfs/etc/dhcpcd.conf
echo "7###########"
cp ${SCRIPT_PATH}/raspberry_settings/raspberry.sh ${HOME}/rootfs/home
echo "8###########"


