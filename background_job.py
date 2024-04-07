import pandas as pd
import mysql.connector as msql
from datetime import date
import time

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# from flightsql import FlightSQLClient

from getpass import getpass
from mysql.connector import connect, Error

try:
    influx_client = influxdb_client.InfluxDBClient(url='http://3.144.28.201:8086', token='vnO1_gFI9YhPTjTMCVo-TA2JPKHJeNF9FSae4DN56Jeou6O8PEglEJ0Fr0egMkD9rKzh52MwYxq4eqCg0Ldleg==',
                                                    org='Americold') 
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    
    temp=0
    while True: 
            p = influxdb_client.Point("climate_change").field("temperature", temp)
            write_api.write(bucket='Test', org='Americold', record=p)
            temp = temp + 1
            time.sleep(2)
            if temp > 110:
                 temp=0
                 write_api.flush()

except Error as e:
    print("Error", e)