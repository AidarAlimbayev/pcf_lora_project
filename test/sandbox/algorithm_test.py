from datetime import datetime, date, time
import time
import socket
import json
import requests
import binascii
import csv
import re
import connect_weight
import collect_data
import connect_id
import send_server

weight = 0
weight_finall = 0
date_now = ''
type_scales = "Scale_A"
row = []

 
def main():
    cow_id = float(connect_id())
    if float(cow_id) != 0:
        weight_finall = float(connect_weight())
        if float(weight_finall) != 0:
            send_server(cow_id, weight_finall)
            collect_data(cow_id, weight_finall)
            main()
        else:
            #return(0)
            main()
    else:
        #return(0)
        main() 

main()