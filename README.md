<!-- #      -->
                                                  ===            
This project started on S.Seifullin University.
Project was founded by Minsitry of Argoculture of Kazakhstan

head of project - Mirmanov Arman mirmanov.a@mail.ru    
main scientific head - Nabiyev Nabi nabi.nabiyev@gmail.com    
engineer - Alimbayev Aidar transcription@rambler.ru    
engineer - Baiguanysh Sanat kvenecusghost@gmail.com
software developer - Maxat Suieubayev maxat.suieubayev@gmail.com

electronics engineer - Damir Gainudinov damirgainudinov@gmail.com

junior sofware developer - Yerkebulan Salmenov salmenov.18.04@gmail.com

junior software developer - Meiirkhan Abdek meiirkhan.abdek@nu.edu.kz

engineer - Vladimir Sarzhinec wowa3520@gmail.com     

Настройка нового Распбери 
============================

* Настроить Ethernet на Распбери 
* 192.168.1.249/24 
* Проверить связь через команду в терминале raspberry pi = ping 192.168.1.250 
* Ручной запуск программы тест
* Проверить калибровку ардуино
* *set_calibration.ino*
* Настроить удаленный доступ
* VNC = pfc.kazatu@gmail.com
* Teamviewer = pcf.kazatu@gmail.com
* Настроить автоматический запуск демона
* Загрузить файл *pcf.service* в __/etc/systemd/system/__
* Загрузить файл *99-serial-logger.rules* в __/etc/udev/rules.d__
* 5-7 раз перезагрузить распбери и проверить статус программы
* 5-7 раз перезагрузить ручным отключением питания
* Перезагрузить с отключенным монитором
* Проверить отключением питания на RFID считвателе
* Проверить появление файла *raw_data.csv*
* Проверить появление лог файла *время_и_дата.log*
* Открыть права на *sudo chown 777 /dev/ttyACM0*
* Проверить программу на работу через 1,3,6,9,25 часов


Код для автоматического запуска программы
-----------------------------------------
[Unit]    
Description=test.service Service       
After=network.target      

[Service]
ExecStart=/usr/bin/python3 /home/pi/main_aid_ver3.py        
WorkingDirectory=/home/pi/        
StandardOutput=inherit    
StandardError=inherit    
Restart=always    
User=root    

[Install]
dBy=multi-user.target        

путь до папки для демона
/etc/systemd/system/    
winSCP    
sudo systemctl start test.service       
sudo systemctl enable test.service       
