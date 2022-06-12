#!/bin/bash


CPU_temp=$(cat /sys/class/thermal/thermal_zone0/temp | cut -c 1-4) 
uis=$(awk '{print $1}' /proc/uptime | awk '{printf("%.f\n",$1)}')
number=$(awk '{print $3}' boot_id.txt)
name=$(whoami)
daemon_en_1=$(systemctl is-enabled pcf.service) 
daemon_ac_1=$(systemctl is-active pcf.service)
#daemon_en_2=$(systemctl is-enabled mysql)
#daemon_ac_2=$(systemctl is-active mysql)
shutdown=$(last -x | head -1 | tail -c 34 | head -c 18)
date=$(date '+%Y-%m-%d %H:%M:%S')

proc_temp=$(bc<<<"scale=1;$CPU_temp / 100")

    if [[ $daemon_en_1 == "enabled" ]]; then
        dep="true"
    else
        dep="false"
    fi
    
    if [[ $daemon_ac_1 == "active" ]]; then
        dap="true"
    else
        dap="false"
    fi


function var_null() {          #Создаем фукнцию для проверки переменной 
    if [ -z ${number+x} ]      #number. Если пустая, то присвоим ей 1
    then                       #и запишем в лог. Т.е. Самое первое вклчение...
        number=1
        echo "id = $number" > /home/pi/boot_id.txt
    fi
}
function var_exist() {         #Функция проверки перезагружалась ли система
    if  (("$uis" < "20"))      #Если да то добавляем +1 к переменной number
    then                       #и записываем в лог
        number=$(($number+1))
        echo "id = $number" > /home/pi/boot_id.txt
    fi
}
set -e

var_null
var_exist
#Здесь будем ловить ошибки
errorCode=$?
if [ $errorCode -ne 0 ]; then
    echo "We have an error" >> errors_log.txt
    #exit $errorCode    #Останавливаем код и выходим. 
                        #Если раскомментить код остановиться.
fi

post_data_to_file() #Функция сбора инфы для log-a и json-a
{
    cat <<EOF
{   
    "EventDate": "$date",
    "SerialNumber": "pcf_model_1",
    "Uptime": "$uis",
    "BootId": "$number",
    "CpuTemp": "$proc_temp",
    "LastShutdown":"$shutdown",
    "ErrorCode": "$errorCode",
    "IsActive": "$dap", 
    "IsEnabled": "$dep"
}
EOF
}
if  (("$uis" < "20"))      #Если система перезагружалась то 
    then                    # записываем в отдельный лог
        
        echo "$(post_data_to_file)" >> /home/pi/Last_shutdown.txt
fi

echo "$(post_data_to_file)" > /home/pi/Desktop/logservice.txt


curl -i \
 -H "Accept: application/json" \
 -H "Content-Type:application/json"\
 -X POST --data "$(post_data_to_file)" "http://smart-farm.kz:8501/v2/SmartScalesStatuses" 

sleep 1m 
