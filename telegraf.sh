#!/bin/bash

# MySQL database connection settings
mysql_host="localhost"
mysql_user="grafanareader"
mysql_password="admin123"
mysql_database="americold"

# Define your SQL query
sql_query="SELECT * FROM dailyTemperature"

# Execute the SQL query and format the output in InfluxDB line protocol format
mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_database" -e "$sql_query" | \
  awk -v measurement="climate_change" 'BEGIN {FS="\t"} NR>1 {print measurement " field1="$1",field2="$2}'
