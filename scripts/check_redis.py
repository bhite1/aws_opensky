import redis

# Redis configuration
redis_host = 'redcluster-ro.5xxacq.ng.0001.use1.cache.amazonaws.com'
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Check if a key exists
key_to_check = 'your_key'
key_exists = redis_client.exists(key_to_check)
if key_exists:
    print(f"The key '{key_to_check}' exists.")
else:
    print(f"The key '{key_to_check}' does not exist.")

# Get data by key
key_to_retrieve = '4b1814'
data = redis_client.get(key_to_retrieve)
if data is not None:
    print(f"Data for '{key_to_retrieve}': {data}")
else:
    print(f"No data found for '{key_to_retrieve}'.")

# List all keys (Caution: Not recommended for large datasets)
all_keys = redis_client.keys('*')
print("All Keys:")
for key in all_keys:
    i = i + 1

print(f"Number of records in Redis: '{i}'.")

