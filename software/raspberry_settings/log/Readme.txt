Это Readme файл для отправки сообщения о состоянии весов на сервер.

Сообщение отправляется с помощью curl. Сообщение представляет из себя строку json. Ниже приведено содержание сообщения. 

    "EventDate": "Дата и время отправки сообщения",
    "SerialNumber": "Имя весов",
    "Uptime": "Время прошедшее после перезагрузки в секундах",
    "BootId": "Кол-во перезагрузок",
    "CpuTemp": "Температура процессора",
    "LastShutdown": "Дата последнего выключения",
    "ErrorCode": "Уловитель ошибок",
    "IsActive": "Проверка демона pcf.service активен", 
    "IsEnabled": "Проверка демона pcf.service включен"


___________________________Краткое рудоководство по установке.____________________________ 

1. Вставляем файлы boot_id.txt и log.sh в /home/pi/Documents/
    1.1 Проверить boot_id. При первом запуске он должен быть равен boot_id = 1.
    1.2 В строке "SerialNumber": "pcf_model_1", изменить имя весов.
2. Вставляем файл log.service в /etc/systemd/system/ (for example from folder in which log.service exsist #~ sudo cp log.service /etc/systemd/system/ )
3. В терминале запустить: 
                            #~ sudo systemctl start log.service
                            #~ sudo systemctl enable log.service

4. Для изменения времени отработки log.sh в файле редактировать последнюю строку sleep 15m на нужное значение 



***Примечание: Нужно разобраться с LastShutdown. 


***Сообщение расширяемое. Свободные строки:
        1. "Memory" : null,
        2. "Battery" : null,
        3. "Voltage" : null,
        4. "ErrorMessage" : null,