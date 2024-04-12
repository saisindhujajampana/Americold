import pandas as pd
import mysql.connector as msql
from datetime import date

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# from flightsql import FlightSQLClient

from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        port=3306,
        user="grafanareader",
        password="admin123",
    ) as connection:
        create_db_query = "CREATE DATABASE online_movie_rating"
except Error as e:
    print(e)

dailyMinTemp = pd.read_csv('resources/sample_temperature_data.csv', index_col=False, delimiter = ',') 

dailyMinTemp.head()

try: 
    conn = connect(host='localhost', port=3306, database='americold', user='grafanareader', password='admin123') 
    if conn.is_connected(): 
        cursor = conn.cursor() 
        cursor.execute("select database();") 
        record = cursor.fetchone() 
        print("You're connected to database: ", record) 
        cursor.execute('DROP TABLE IF EXISTS dailyTemperature;') 
        print('Creating table....') 
        # in the below line please pass the create table statement which you want #to create 
        cursor.execute("CREATE TABLE dailyTemperature(date DATE NOT NULL,min_temperature DECIMAL(6,2))") 
        print("Table is created....") 
        #loop through the data frame for i,row in empdata.iterrows(): #here %S means string values 
        sql = "INSERT INTO americold.dailyTemperature VALUES (%s,%s,%s)" 
    
        for i,j in dailyMinTemp.iterrows():
            now = j['Date'].split("/")
            dateObj = date(int("19"+now[2]), int(now[0]), int(now[1]))
            cursor.execute(sql, (dateObj.strftime('%Y-%m-%d'), j['Daily minimum temperatures'])) 
            
    conn.commit()


except Error as e: 
    print("Error while connecting to MySQL", e)


# -- now connect to InfluxDB


try:
    influx_client = influxdb_client.InfluxDBClient(url='http://3.144.28.201:8086', token='vnO1_gFI9YhPTjTMCVo-TA2JPKHJeNF9FSae4DN56Jeou6O8PEglEJ0Fr0egMkD9rKzh52MwYxq4eqCg0Ldleg==',
                                                    org='Americold') 
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    
    conn = connect(host='localhost', port=3306, database='americold', user='grafanareader', password='admin123') 
    if conn.is_connected(): 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dailyTemperature;')
        for row in cursor:
            p = influxdb_client.Point("climate_change").field("temperature", row[1]).field("date", row[0].strftime('%m/%d/%Y'))
            write_api.write(bucket='Test', org='Americold', record=p)
        write_api.flush()

except Error as e:
    print("Error", e)