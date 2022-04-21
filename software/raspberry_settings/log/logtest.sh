#!/bin/bash

#proc_temp=$(vcgencmd measure_temp)      "CPU_Temperature": "$proc_temp"
name=$(whoami)
time=$(uptime | head -c 18 )
we=300
sm=now

post_data()
{
    cat <<EOF
{   
    "AnimalNumber" : "$name",
    "Date" : "2022-04-21 19:17:46.353119",
    "Weight" : "$we",
    "ScalesModel" : "$sm"
}
EOF
}


curl -i \
 -H "Accept: application/json" \
 -H "Content-Type:application/json"\
 -X POST --data "$(post_data)" "https://smart-farm.kz:8500/api/weights"