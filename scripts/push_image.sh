#!/usr/bin/env bash

docker build -t zipcode_service_dev:latest .
aws_account_id=`aws sts get-caller-identity --query "Account" --output text`
docker tag zipcode_service_dev:latest $aws_account_id.dkr.ecr.us-east-1.amazonaws.com/zipcode_service_dev:latest
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.us-east-1.amazonaws.com
docker push $aws_account_id.dkr.ecr.us-east-1.amazonaws.com/zipcode_service_dev:latest
