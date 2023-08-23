import json
import requests
import boto3
from decimal import Decimal
from datetime import datetime

# Initialize a session using Amazon DynamoDB
session = boto3.Session(region_name='us-east-1')

# Initialize DynamoDB resource
dynamodb = session.resource('dynamodb')

# DynamoDB table
table = dynamodb.Table('aircraftdb')

def lambda_handler(event, context):
    try:
        # Fetch data from OpenSky API
        response = requests.get('https://opensky-network.org/api/states/all')
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # 'states' is the key containing the array of events
            # Limit the output to 10 records for testing
            states = data.get('states', [])[:10]
            
            # Current timestamp as a Unix timestamp
            current_time = int(datetime.now().timestamp())
            
            for state in states:
                event = {
                    'timestamp': current_time,
                    'icao24': state[0],
                    'callsign': state[1],
                    'origin_country': state[2],
                    'time_position': Decimal(str(state[3])) if state[3] else None,
                    'last_contact': Decimal(str(state[4])) if state[4] else None,
                    'longitude': Decimal(str(state[5])) if state[5] else None,
                    'latitude': Decimal(str(state[6])) if state[6] else None,
                    'baro_altitude': Decimal(str(state[7])) if state[7] else None,
                    'on_ground': state[8],
                    'velocity': Decimal(str(state[9])) if state[9] else None,
                    'true_track': Decimal(str(state[10])) if state[10] else None,
                    'vertical_rate': Decimal(str(state[11])) if state[11] else None,
                    'sensors': state[12],
                    'geo_altitude': Decimal(str(state[13])) if state[13] else None,
                    'squawk': state[14],
                    'spi': state[15],
                    'position_source': state[16]
                }
                
                # Write the event to DynamoDB
                table.put_item(Item=event)
            
            return {
                'statusCode': 200,
                'body': json.dumps(f"Data saved to DynamoDB for timestamp {current_time}")
            }
        
        else:
            return {
                'statusCode': 500,
                'body': json.dumps(f"Failed to get data from OpenSky API. Status code: {response.status_code}")
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }

