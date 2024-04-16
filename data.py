import pymysql
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# MySQL connection parameters
mysql_host = 'localhost'
mysql_port = 3306
mysql_user = 'grafanareader'
mysql_password = 'admin123'
mysql_db = 'americold'

# InfluxDB connection parameters
influxdb_url = '3.144.28.201'
influxdb_port = 8086
influxdb_user = 'InfluxDB'
influxdb_password = 'admin123'
influxdb_db = 'americold'

def migrate_data():
    # Connect to MySQL
    mysql_conn = pymysql.connect(host=mysql_host,
                                 port=mysql_port,
                                 user=mysql_user,
                                 password=mysql_password,
                                 db=mysql_db,
                                 cursorclass=pymysql.cursors.DictCursor)

    # Connect to InfluxDB
    influx_client = influxdb_client.InfluxDBClient(url='http://3.144.28.201:8086', token='vnO1_gFI9YhPTjTMCVo-TA2JPKHJeNF9FSae4DN56Jeou6O8PEglEJ0Fr0egMkD9rKzh52MwYxq4eqCg0Ldleg==',
                                                    org='Americold')
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    # Fetch data from MySQL
    with mysql_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM rochelle")
        rows = cursor.fetchall()
        print("Fetched rows from MySQL:")
        print(rows)
        for row in rows:
            epochTime = row['Timestamp'].timestamp()
            epochTime = datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S').timestamp()
            #epochTime = datetime.strptime(row['Timestamp'], '%y-%m-%d %H:%M:%S').timestamp()
            dictionary = {
                "measurement": "temperature",
                "tags": {
                    "zone": row["Zone"],
                    "sub_zone": row["Sub-zone"],
                    "status": row["Status"]
                },
                "fields": {
                    "temperature": row["Temperature (°C)"],
                    "pressure": row["Pressure (hPa)"]
                },
                "time": int(epochTime)
            }
            point = influxdb_client.Point.from_dict(dictionary, influxdb_client.WritePrecision.S)
            write_api.write(bucket='Rochelle', org='Americold', record=point)

    write_api.flush()
    # Write data to InfluxDB
    # write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    # influxdb_client.
    # influxdb_client.write_points(influx_data)

    # Close connections
    mysql_conn.close()

def main():
    while True:
        # Sample SQL query
        sql_query = "SELECT * FROM rochelle WHERE timestamp > (NOW() - INTERVAL 1 MINUTE);"
        # Read data from SQL
        data = read_from_sql(sql_query)
        if not data.empty:
            # Convert DataFrame to InfluxDB JSON format
            influx_data = data.to_json(orient='records')
            # Write data to InfluxDB
            write_to_influxdb(influx_data)
        # Wait for 5 minutes before checking again
        time.sleep(300)

if __name__ == "__main__":
    migrate_data()