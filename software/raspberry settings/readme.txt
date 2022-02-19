***First set up Wi-Fi on Raspberry without screen***
!! - means bash code which you should to enter to the terminal. 

Password for super pi.user: 12345

1. Downoload Raspberry Pi Imager https://www.raspberrypi.com/software/

2. Run downoload file

3. Choose SD cart

4. Choose OS (if you want to install another OS you can downoload it on 
https://www.raspberrypi.com/software/operating-systems/)

5. Open SD cart's boot, then create 2 new files:    - ssh (without format)  !!  touch ssh
                                                                                sudo chmod +x ssh

                                                    - wpa_supplicant.conf   !!  touch wpa_supplicant.conf
                                                                                sudo chmod +x wpa_supplicant.conf

6. Open wpa_supplicant.conf on any text editor(for example nano) and add next configure:
!! nano wpa_supplicant.conf

country=KZ
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="Your Wi-Fi name"
    psk="Your Wi-Fi Password"
    key_mgmt=WPA-PSK
}

6. Erase SD
7. Put SD to raspberrypi and turn it on
8. Wait 1-3 min, then you can check connection !! ping pi@raspberrypi.local
    8.1 If that's not work you can also check on your router settings (192.168.$1.$1) raspberry's ip address. For example $ip=192.168.1.100
9. ssh pi@192.168.1.100
    9.1 Or use putty 
10. Pass: "raspberry"
11. Install tightvncserver !! sudo apt-get install tightvncserver
                            $New_Password 
12. !! tightvncserver

13. If msg "New 'X' desktop is raspberrypi:2" thats means you are on the way. 

14. ctrl+alt+t and new terminal and call remmina !! remmina
    14.1 If you don't have remmina first enter  !!sudo apt update
                                                !!sudo apt install remmina
15. CLick to "+" on left side of the bar. In Protocl choose Module(plugin) VNC Remmina. In server enter raspberry's $ip+port(For example :1) address Save and connect.
16. Enter $New_Password. 