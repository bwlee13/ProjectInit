import boto3
from botocore.exceptions import ClientError
import os
import json
from decimal import Decimal
from pprint import pprint
from loguru import logger
import pandas as pd


dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")


def load_data(users):
    devices_table = dynamodb.Table('Users')
    # Loop through all the items and load each
    for user in users:
        userId = (user['userId'])
        firstName = user['firstName']
        lastName = user['lastName']
        bookList = user['bookList']
        followerList = user['followerList']
        follwingList = user['followingList']
        acctData = user['acctData']
        # Print device info
        print("Loading Devices Data:", userId, firstName, lastName, bookList, followerList, follwingList, acctData )
        devices_table.put_item(Item=user)


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
    table = dynamodb.create_table(
        TableName='Users',
        KeySchema=[
            {'AttributeName': 'userId', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'userId', 'AttributeType': 'S'},
            # {'AttributeName': 'firstName', 'AttributeType': 'S'},
            # {'AttributeName': 'lastName', 'AttributeType': 'S'},
            # {'AttributeName': 'bookList', 'AttributeType': 'S'},
            # {'AttributeName': 'followerList', 'AttributeType': 'S'},
            # {'AttributeName': 'follwingList', 'AttributeType': 'S'},
            # {'AttributeName': 'acctData', 'AttributeType': 'S'},

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
    )
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


def get_user_account(user_id):
    # Specify the table to read from
    user_table = dynamodb.Table('Users')
    try:
        response = user_table.get_item(
            Key={'userId': user_id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


def scan_devices():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to scan
    devices_table = dynamodb.Table('Users')
    response = devices_table.scan()
    print(response)
    items = response['Items']
    while 'LastEvaluatedKey' in response:
        print(response['LastEvaluatedKey'])
        response = devices_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    print(items)


if __name__ == '__main__':
    # device_table = create_user_table()
    # # Print table status
    # print("Status:", device_table.table_status)
    #
    # with open("../userdata.json") as json_file:
    #     device_list = json.load(json_file, parse_float=Decimal)
    # load_data(device_list)

    # device_resp = put_device("10001", 3, "1612522800",
    #                          "23.74", "32.56", "12.43", "44.74", "12.74")
    # print("Create item successful.")
    # # Print response
    # pprint(device_resp)

    user = get_user_account("bwlee13")
    if user:
        print("Get Device Data Done:")
        # Print the data read
        print(user)

    # scan_devices()

