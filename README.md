# aws_opensky

# Setup

1. IAM role named Lambda2DynamoDB

* Permissions policies
  * AmazonDynamoDBFullAccess
  * AWSLambdaBasicExecutionRole

2. Zip the Python requests package
```
mkdir python
pip install requests -t ./python
zip -r requests_layer.zip ./python
```

3. Create the Lambda function

* Add an EventBridge rule called Trigger-5min-Lambda with an event schedule of rate(5 minutes)
* Attach the IAM role
* Add a Layer to the function and include requests_layer.zip

4. Setup DynamoDB

* table: aircraftdb
* partition key: timestamp (N)
* sort key: icao24 (S)
