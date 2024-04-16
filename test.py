import mysql.connector
import random
import time
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Function to generate random data for demonstration purposes
def generate_random_data():
    zones = ['Zone A', 'Zone B', 'Zone C']
    sub_zones = ['Subzone 1', 'Subzone 2', 'Subzone 3']
    statuses = ['Up', 'Down', 'Maintenance']
    pressure = round(random.uniform(10, 60), 2)
    temperature = round(random.uniform(800, 1000), 2)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return random.choice(zones), random.choice(sub_zones), random.choice(statuses), pressure, temperature, timestamp

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="grafanareader",
        password="admin123",
        database="americold"
    )
    cursor = conn.cursor()

    print("Connected to MySQL database.")

    # Continuous data insertion
    while True:
        # Generate random data
        zone, sub_zone, status, pressure, temperature, Timestamp = generate_random_data()

        # SQL query to insert data
        sql = "INSERT INTO rochelle (zone, sub_zone, status, pressure, temperature, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (zone, sub_zone, status, pressure, temperature, Timestamp)

        # Execute the SQL query
        cursor.execute(sql, val)
        conn.commit()

        print("Inserted data into the database.")

        # Wait for 1 seconds before inserting the next data
        time.sleep(1)

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")

