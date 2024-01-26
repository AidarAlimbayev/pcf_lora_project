#!/bin/bash

# константы для путей к файлам и имен сервисов для удобства обновления и обслуживания.
THERMAL_ZONE_PATH="/sys/class/thermal/thermal_zone0/temp"
UPTIME_PATH="/proc/uptime"
BOOT_ID_FILE="/home/pi/Documents/boot_id.txt"
LOGSERVICE_FILE="/home/pi/Documents/logservice.txt"
LAST_SHUTDOWN_FILE="/home/pi/Documents/Last_shutdown.txt"
ERRORS_LOG_FILE="/home/pi/Documents/errors_log.txt"
PCF_SERVICE="pcf.service"

# Получить системную информацию.
CPU_temp=$(cut -c 1-4 < "$THERMAL_ZONE_PATH")
uis=$(awk '{print $1}' "$UPTIME_PATH" | awk '{printf("%.f\n",$1)}')
number=$(awk '{print $3}' "$BOOT_ID_FILE")
daemon_en_1=$(systemctl is-enabled "$PCF_SERVICE") 
daemon_ac_1=$(systemctl is-active "$PCF_SERVICE")
shutdown=$(last -x | head -1 | tail -c 34 | head -c 18)
date=$(date '+%Y-%m-%d %H:%M:%S')
proc_temp=$(bc <<< "scale=1;$CPU_temp/100")

# булевы флаги для статуса сервиса.
dep=$([[ $daemon_en_1 == "enabled" ]] && echo "true" || echo "false")
dap=$([[ $daemon_ac_1 == "active" ]] && echo "true" || echo "false")

# Проверить, существует ли файл boot_id.txt и не пуст ли он.
var_null() {
    if [ -z "${number+x}" ]; then
        number=1
        echo "id = $number" > "$BOOT_ID_FILE"
    fi
}

# Увеличить номер загрузки, если система была перезагружена недавно.
var_exist() {
    if  ((uis < 10)); then
        number=$((number+1))
        echo "id = $number" > "$BOOT_ID_FILE"
    fi
}

# Функция для поиска config.ini и возвращения его полного пути.
find_config_file() {
    local result=$(find / -name "config.ini" 2>/dev/null)
    echo "$result"
}

# Функция для чтения SerialNumber из найденного config.ini.
get_serial_number() {
    local config_path=$1
    local serial_number=$(awk -F " = " '/serial_number/ {print $2}' "$config_path")
    echo "$serial_number"
}

# Находим путь к config.ini.
config_file=$(find_config_file)

# Если файл найден, извлекаем SerialNumber.
if [[ -n $config_file ]]; then
    serial_number=$(get_serial_number "$config_file")
    echo "Найденный серийный номер: $serial_number"
else
    echo "Файл config.ini не найден."
fi

# Установить обработку ошибок.
set -e

var_null
var_exist

# Перехват ошибок.
errorCode=$?
if [ $errorCode -ne 0 ]; then
    echo "У нас ошибка" >> "$ERRORS_LOG_FILE"
fi

# Функция для компиляции данных в формат JSON.
post_data_to_file() {
    cat <<EOF
{   
    "EventDate": "$date",
    "SerialNumber": "$serial_number",
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

# Записать данные в разные файлы в зависимости от времени работы системы.
if  ((uis < 10)); then
    post_data_to_file >> "$LAST_SHUTDOWN_FILE"
fi

post_data_to_file > "$LOGSERVICE_FILE"

# Отправить данные на удаленный сервер.
curl -i \
 -H "Accept: application/json" \
 -H "Content-Type:application/json" \
 -X POST --data "$(post_data_to_file)" "http://smart-farm.kz:8501/v2/SmartScalesStatuses"

# Ожидание 15 минут перед следующим выполнением.
sleep 15m
