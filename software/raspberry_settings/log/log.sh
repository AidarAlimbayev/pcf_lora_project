#!/bin/bash

proc_temp=$(vcgencmd measure_temp)      
name=$(whoami)
time=$(uptime | head -c 18 )

post_data()
{
    cat <<EOF
{   
    "Scales_Model": "$name"
    "CPU_Temperature": "$proc_temp"
    "Uptime_Since_First":"$time"
}
EOF
}

curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data "$(post_data)" "http://194.4.56.86:8501/api/weights"
