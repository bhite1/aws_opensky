import csv
import json
import redis

# Redis configuration
redis_host = 'testcluster-001.5xxacq.0001.use1.cache.amazonaws.com'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Test Redis connectivity
try:
    response = redis_client.ping()

    if response:
        print("Connected to Redis cluster successfully.")
    else:
        print("Failed to connect to Redis cluster.")
except redis.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

# Path to the CSV file
csv_file_path = 'aircraftDatabase.csv'

# Read and load data from CSV into Redis
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        aircraft_registration = row['registration']

        row_json = json.dumps(row)

        # Store the data in Redis (using SET command)
        redis_client.set(aircraft_registration, row_json)

        # Or if you want to use Redis hashes
        # redis_client.hmset(aircraft_registration, row)

