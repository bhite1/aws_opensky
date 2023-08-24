#!/bin/bash

# Set AWS CLI default region (change as needed)
region="us-east-1"
bucketName="HackyBucketsAreNeat"
stackName="ParentStack"
deployTemplate="./deploy.json"

# Create S3 bucket
aws s3api create-bucket --bucket $bucketName --region $region

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
