# pcf_lora_project

This project started on S.Seifullin University.
Project was founded by Minsitry of Argoculture of Kazakhstan

head of project - Mirmanov Arman mirmanov.a@mail.ru
main scientific head - Nabiyev Nabi nabi.nabiyev@gmail.com
engineer - Alimbayev Aidar transcription@rambler.ru
engineer - Baiguanysh Sanat kvenecusghost@gmail.com 

Настроить Ethernet на Распбери 
192.168.1.249/24 
Raspberry pi = ping 192.168.1.250 
Ручной запуск программы тест
Проверить калибровку ардуино
Настроить удаленный доступ
VNC = astana.integration@gmail.com
Teamviewer = aidar.alimbayev@nu.edu.kz
Настроить автоматический запуск демона
5-7 раз перезагрузить распбери и проверить статус программы
5-7 раз перезагрузить ручным отключением питания
Перезагрузить с отключенным монитором
Проверить отключением питания на RFID считвателе
Проверить появление файла raw_data.csv
Открыть права на ttyACM0 chown
Проверить программу на работу через 1,3,6,9,25 часов


Модули которые нужно добавить и ошибки которые нужно исправить

Отправка данных при появлении сети WiFi или 4G
Логирование данных с программы в файл systemctl +
Перевод RFID считывателя на USB 
Мягкое выключение через ИБП с сигналом отключения на Rasberry
Исправить кода на отправку 0 веса к серверу 
Оставить десятые доли на значении веса которые отправляются
Установка мощности антенны перед началом программы функция установки
Поставить больше равно на проверку веса
Права для программы root sudo
Отдельное питание для Ардуино
Закрывать файл после записи, проверить повторное открытие файла
Проверить правильность функции открытия и записи файлов csv. 
Установка времени на логирование +
Почему не работает продолжительное время?
Проверить какие функции занимают порт ардуино
Проверить weight_list != [] lib -> 34 строка


Код для автоматического запуска программы
[9:06 PM, 6/1/2020] . S: [Unit]
Description=Sheala_B Service
After=network.target

[Service]
ExecStart=/usr/bin/python /opt/sheala_b/rx_cont.py
WorkingDirectory=/opt/sheala_b
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
[9:09 PM, 6/1/2020] . S: /etc/systemd/system/
[9:14 PM, 6/1/2020] . S: winSCP
[9:16 PM, 6/1/2020] . S: sudo systemctl start sheala_b.service
[9:22 PM, 6/1/2020] . S: sudo systemctl enable sheala_b.service
