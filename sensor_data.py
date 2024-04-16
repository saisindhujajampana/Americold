import csv
import random
from datetime import datetime, timedelta

# Define zones, sub-zones, and status
zones = ['Zone A', 'Zone B', 'Zone C']
sub_zones = ['Sub-zone 1', 'Sub-zone 2', 'Sub-zone 3']
status = ['Up', 'Down', 'maintenance']

# Function to generate random data for temperature, pressure, and timestamp
def generate_data():
    temperature = round(random.uniform(10, 60), 2)  # Temperature between 10°C and 40°C
    pressure = round(random.uniform(800, 1200), 2)  # Pressure between 800 hPa and 1200 hPa
    timestamp = datetime.now() - timedelta(days=random.randint(0, 20))
    return temperature, pressure, timestamp

# Generate CSV file
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Zone', 'Sub-zone', 'Status', 'Temperature (°C)', 'Pressure (hPa)', 'Timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for _ in range(100):  # Generate 100 records
        zone = random.choice(zones)
        sub_zone = random.choice(sub_zones)
        status_value = random.choice(status)
        temperature, pressure, timestamp = generate_data()
        writer.writerow({
            'Zone': zone,
            'Sub-zone': sub_zone,
            'Status': status_value,
            'Temperature (°C)': temperature,
            'Pressure (hPa)': pressure,
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

print("CSV file generated successfully.")