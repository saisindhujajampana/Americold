import mysql.connector
import csv
from datetime import datetime

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='grafanareader',
    password='admin123',
    database='americold'
)
cursor = conn.cursor()

# Create table to store mechatronics data
create_table_query = '''
    CREATE TABLE IF NOT EXISTS MechatronicsData (
        Timestamp DATETIME,
        Daily_minimum_temperatures FLOAT,
        Pressure FLOAT,
        Current FLOAT,
        Voltage FLOAT
    )
'''
cursor.execute(create_table_query)

# Read data from CSV file and insert into the database
with open('resources/data.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for line_num, row in enumerate(csvreader, 2):  # Start counting at line 2
        if len(row) != 5:  # Check if number of columns is correct
            print(f"Error: Row {line_num} does not contain the expected number of columns.")
            print(f"Row {line_num}: {row}")
            continue  # Skip this row and mov to the next one
        try:
            insert_query = '''
                INSERT INTO MechatronicsData 
                VALUES (%s, %s, %s, %s, %s)
            '''
            # Convert values to appropriate data types
            values = (
                timestamp, float(row[1]) if row[1] else None, float(row[2]) if row[2] else None, 
                float(row[3]) if row[3] else None, float(row[4]) if row[4] else None
            )
            cursor.execute(insert_query, values)
        except Exception as e:
            print(f"Error inserting data from row {line_num}: {e}")

# Commit changes and close connection
conn.commit()
conn.close()

print("Data inserted into MySQL database successfully.")