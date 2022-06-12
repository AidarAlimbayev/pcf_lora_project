#!/bin/bash

number=$(awk '{print $3}' boot_id.txt)

function var_null() {          #Создаем фукнцию для проверки переменной 
    if [ -z ${number+x} ]      #number. Если пустая, то присвоим ей 1
    then                       #и запишем в лог. Т.е. Самое первое вклчение...
        number=1
        echo "id = $number" > /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/log/boot_id.txt
    fi
}
function var_exist() {         #Функция проверки перезагружалась ли система
    if  (("1" < "600"))      #Если да то добавляем +1 к переменной number
    then                       #и записываем в лог
        number=$(($number+1))
        echo "id = $number" > /home/maxat/.Projects/.Agrarka/pcf_lora_project/software/raspberry_settings/log/boot_id.txt
    fi
}

var_null
var_exist