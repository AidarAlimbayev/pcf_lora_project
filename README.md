# pcf_lora_project

This project started on S.Seifullin University.
Project was founded by Minsitry of Argoculture of Kazakhstan

head of project - Mirmanov Arman mirmanov.a@mail.ru    
main scientific head - Nabiyev Nabi nabi.nabiyev@gmail.com    
engineer - Alimbayev Aidar transcription@rambler.ru    
engineer - Baiguanysh Sanat kvenecusghost@gmail.com     

Настройка нового Распбери 
============================

* Настроить Ethernet на Распбери 
* 192.168.1.249/24 
* Raspberry pi = ping 192.168.1.250 
* Ручной запуск программы тест
* Проверить калибровку ардуино
* Настроить удаленный доступ
* VNC = astana.integration@gmail.com
* Teamviewer = aidar.alimbayev@nu.edu.kz
* Настроить автоматический запуск демона
* Загрузить файл *test.service* в __/etc/systemd/system/__
* Загрузить файл *99-serial-logger.rules* в __/etc/udev/rules.d__
* 5-7 раз перезагрузить распбери и проверить статус программы
* 5-7 раз перезагрузить ручным отключением питания
* Перезагрузить с отключенным монитором
* Проверить отключением питания на RFID считвателе
* Проверить появление файла *raw_data.csv*
* Проверить появление лог файла *время_и_дата.log*
* Открыть права на *ttyACM0 chown*
* Проверить программу на работу через 1,3,6,9,25 часов

Модули которые нужно добавить и ошибки которые нужно исправить
-----------------------------------------------------------------

:black_square_button: Отправка данных при появлении сети WiFi или 4G    
:white_check_mark: Логирование данных с программы в файл systemctl +    
:black_square_button: Перевод RFID считывателя на USB     
:black_square_button: Мягкое выключение через ИБП с сигналом отключения на Rasberry    
:black_square_button: Исправить кода на отправку 0 веса к серверу     
:black_square_button: Оставить десятые доли на значении веса которые отправляются    
:black_square_button: Установка мощности антенны перед началом программы функция установки    
:black_square_button: Поставить больше равно на проверку веса    
:white_check_mark: Права для программы root sudo    
:black_square_button: Отдельное питание для Ардуино    
:black_square_button: Закрывать файл после записи, проверить повторное открытие файла    
:black_square_button: Проверить правильность функции открытия и записи файлов csv.     
:white_check_mark: Установка времени на логирование +       
:white_check_mark: Почему не работает продолжительное время?    
:black_square_button: Проверить какие функции занимают порт ардуино    
:black_square_button: Проверить weight_list != [] lib -> 34 строка    
:black_square_button: Отправка тестового пакета при включении или перегрузки    
:black_square_button: Отправка идентификационного пакета при отсутсвии связи с весами     
:black_square_button: Отправка данных через LoRa32u4    

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

/etc/systemd/system/    
winSCP    
sudo systemctl start test.service       
sudo systemctl enable test.service       
