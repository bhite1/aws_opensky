#!/bin/bash

# Set AWS CLI default region (change as needed)
region="us-west-2"
bucketName="hackybucketsareneat"
stackName="ParentStack"
deployTemplate="./Deploy.json"

# Create S3 bucket
aws s3api create-bucket --bucket $bucketName --region $region

# Wait for the S3 bucket to be confirmed as existing
echo "Waiting for bucket to be created..."
while [[ $(aws s3api head-bucket --bucket $bucketName 2>&1) ]]; do
  echo -n '.'
  sleep 2
done
echo -e "\nBucket created."

# Sync CloudFormation child templates to the S3 bucket
aws s3 cp ./dynamodb.json s3://$bucketName/
aws s3 cp ./ec2.json s3://$bucketName/
aws s3 cp ./iam-ec2.json s3://$bucketName/
aws s3 cp ./iam-lambda.json s3://$bucketName/
aws s3 cp ./lambda-function.json s3://$bucketName/
aws s3 cp ./lambda-layer.json s3://$bucketName/
aws s3 cp ./s3.json s3://$bucketName/

# Deploy CloudFormation parent stack
aws cloudformation create-stack --stack-name $stackName --template-body file://$deployTemplate --parameters ParameterKey=BucketName,ParameterValue=$bucketName --capabilities CAPABILITY_NAMED_IAM
