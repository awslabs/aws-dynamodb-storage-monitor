## AWS Dynamodb Storage Monitor

A Python code (Lambda function) which will help to get storage info all DynamoDB tables in a region and publish that metrics in CloudWatch periodically. A cloudFormation template - Since DynamoDb do not have any storage metrics - this CF template will help customer to trigger the Lambda code (Python code) in every 6 hours to push storage utilization info to cloudWatch

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
