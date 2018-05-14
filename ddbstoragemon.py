# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
# version 0.1


from __future__ import print_function
from datetime import date, datetime, timedelta
import json
import boto3
import time
from botocore.exceptions import ClientError
import os

ddbRegion = os.environ['AWS_DEFAULT_REGION']
#ddbTable = 'hashrange'
ddbClient = boto3.client('dynamodb', region_name=ddbRegion)


cwClient = boto3.client('cloudwatch')

def lambda_handler(event, context):
    
    response = ddbClient.list_tables()
    if 'LastEvaluatedTableName' in response:
        LastEvaluatedTableName = response['LastEvaluatedTableName']
    else:
        LastEvaluatedTableName = ''
    
    listTables=response['TableNames']
    for tablename in listTables:
        responseTableSize= ddbClient.describe_table(TableName=tablename)
        TableSizeBytes=responseTableSize['Table']['TableSizeBytes']
        print(tablename,'-',responseTableSize['Table']['TableSizeBytes'])
        responseCW = cwClient.put_metric_data(Namespace='DynamoDBStorageMetrics',
            MetricData=[
                {
                    'MetricName': 'StorageMetrics',
                    'Dimensions': [
                        {
                            'Name': 'tablename',
                            'Value': tablename
                        },
                    ],
                    'Timestamp': datetime.now(),
                    'Value': TableSizeBytes,
                    'Unit': 'Bytes',
                    'StorageResolution': 1
                },
            ]
            )
        
			
    while (LastEvaluatedTableName != ''):
        response = ddbClient.list_tables(ExclusiveStartTableName=LastEvaluatedTableName)
        if 'LastEvaluatedTableName' in response:
            LastEvaluatedTableName = response['LastEvaluatedTableName']
        else:
            LastEvaluatedTableName = ''
            
        listTables=response['TableNames']
        for tablename in listTables:
            responseTableSize= ddbClient.describe_table(TableName=tablename)
            TableSizeBytes=responseTableSize['Table']['TableSizeBytes']
            print(tablename,'-',responseTableSize['Table']['TableSizeBytes'])
    
            responseCW = cwClient.put_metric_data(Namespace='DynamoDBStorageMetrics',
            MetricData=[
                {
                    'MetricName': 'StorageMetrics',
                    'Dimensions': [
                        {
                            'Name': 'tablename',
                            'Value': tablename
                        },
                    ],
                    'Timestamp': datetime.now(),
                    'Value': TableSizeBytes,
                    'Unit': 'Bytes',
                    'StorageResolution': 1
                },
            ]
            )
    

