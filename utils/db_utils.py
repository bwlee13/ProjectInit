import boto3
from botocore.exceptions import ClientError
import os
import json
from decimal import Decimal
from pprint import pprint
from loguru import logger

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")


def load_data(devices, dynamodb=None):
    devices_table = dynamodb.Table('Devices')
    # Loop through all the items and load each
    for device in devices:
        device_id = (device['device_id'])
        datacount = device['datacount']
        # Print device info
        print("Loading Devices Data:", device_id, datacount)
        devices_table.put_item(Item=device)


def create_devices_table(dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Table defination
    table = dynamodb.create_table(
        TableName='Devices',
        KeySchema=[
            {
                'AttributeName': 'device_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'datacount',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'device_id',
                # AttributeType defines the data type. 'S' is string type and 'N' is number type
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'datacount',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table


def create_user_table():
    table_name = 'Users'
    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': 'partition_key', 'KeyType': 'HASH'},
            {'AttributeName': 'sort_key', 'KeyType': 'RANGE'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'partition_key', 'AttributeType': 'N'},
            {'AttributeName': 'sort_key', 'AttributeType': 'N'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapcityUnits': 10
        },
    }
    table = dynamodb.create_table(**params)
    logger.info(f"Creating table: {table_name}")
    table.wait_until_exists()
    return table


def put_device(device_id, datacount, timestamp, temperature1, temperature2, temperature3, temperature4, temperature5, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table
    devices_table = dynamodb.Table('Devices')
    response = devices_table.put_item(
        # Data to be inserted
        Item={
            'device_id': device_id,
            'datacount': datacount,
            'info': {
                'info_timestamp': timestamp,
                'temperature1': temperature1,
                'temperature2': temperature2,
                'temperature3': temperature3,
                'temperature4': temperature4,
                'temperature5': temperature5
            }
        }
    )
    return response


def get_device(device_id, datacount):
    # Specify the table to read from
    devices_table = dynamodb.Table('Devices')

    try:
        response = devices_table.get_item(
            Key={'device_id': device_id, 'datacount': datacount})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def scan_devices():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to scan
    devices_table = dynamodb.Table('Devices')
    response = devices_table.scan()
    print(response)
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        print(response['LastEvaluatedKey'])
        response = devices_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    print(items)


if __name__ == '__main__':
    # device_table = create_devices_table()
    # Print table status
    # print("Status:", device_table.table_status)

    # with open("../data.json") as json_file:
    #     device_list = json.load(json_file, parse_float=Decimal)
    # load_data(device_list)

    # device_resp = put_device("10001", 3, "1612522800",
    #                          "23.74", "32.56", "12.43", "44.74", "12.74")
    # print("Create item successful.")
    # # Print response
    # pprint(device_resp)

    device = get_device("10001", 3, )
    if device:
        print("Get Device Data Done:")
        # Print the data read
        print(device)

    # scan_devices()

