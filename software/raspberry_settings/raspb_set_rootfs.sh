#!/usr/bin/env bash                                                                       
set -Eeuo pipefail
SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/../" &> /dev/null && pwd )
#SD=$( cd "/media/$USER" ; pwd )


#mkdir /media/maxat/rootfs/home/pi/scales_without_sprayer

cp ${SCRIPT_PATH}/raspberry_settings/ssh /media/maxat/boot2
chmod +x /media/maxat/boot2/ssh
echo "1#############"

cp ${SCRIPT_PATH}/raspberry_settings/wpa_supplicant.conf /media/maxat/boot2
chmod +x /media/maxat/boot2/wpa_supplicant.conf
echo "2#############"

cp ${SCRIPT_PATH}/main/max_scales/scales_without_sprayer/headers.py /media/maxat/rootfs/home/pi/
chmod 777 /media/maxat/rootfs/home/pi/headers.py
echo `ls -l` /media/maxat/rootfs/home/pi/headers.py
echo "3#############"

cp ${SCRIPT_PATH}/main/max_scales/scales_without_sprayer/main_pcf.py /media/maxat/rootfs/home/pi/
chmod 777 /media/maxat/rootfs/home/pi/main_pcf.py
echo "4#############"

cp ${SCRIPT_PATH}/main/max_scales/scales_without_sprayer/lib_pcf.py /media/maxat/rootfs/home/pi/
chmod 777 /media/maxat/rootfs/home/pi/lib_pcf.py
echo "4#############"

cp ${SCRIPT_PATH}/main/pcf.service /media/maxat/rootfs/etc/systemd/system
chmod 777 /media/maxat/rootfs/etc/systemd/system/pcf.service
echo "5#############"

cp ${SCRIPT_PATH}/main/99-serial-logger.rules /media/maxat/rootfs/etc/udev/rules.d
chmod 777 /media/maxat/rootfs/etc/udev/rules.d/99-serial-logger.rules
echo "6#############"

chmod 777 /media/maxat/rootfs/etc/dhcpcd.conf
cat ${SCRIPT_PATH}/raspberry_settings/dhcpcd.conf > /media/maxat/rootfs/etc/dhcpcd.conf
echo "7###########"

cp ${SCRIPT_PATH}/raspberry_settings/raspberry.sh /media/maxat/rootfs/home
echo "8###########"


