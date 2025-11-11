import json
import boto3
import pytest
from moto import mock_aws
from app import put_function

TEST_TABLE_NAME = 'resume-website-visitor-counter'

@mock_aws
def test_put_function_increments_count():

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=TEST_TABLE_NAME,
        KeySchema=[{'AttributeName': 'ID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'ID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    
    initial_count = 5
    dynamodb.Table(TEST_TABLE_NAME).put_item(
        Item={'ID': 'visit_count', 'visit_count': initial_count}
    )

    event = {}
    context = {}
    result = put_function(event, context)

    assert result['statusCode'] == 200

    body = json.loads(result['body'])
    expected_new_count = initial_count + 1
    assert body['count'] == expected_new_count

    table = dynamodb.Table(TEST_TABLE_NAME)
    response = table.get_item(Key={'ID': 'visit_count'})
    assert response['Item']['visit_count'] == expected_new_count


@mock_aws
def test_put_function_initializes_count_if_missing():

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=TEST_TABLE_NAME,
        KeySchema=[{'AttributeName': 'ID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'ID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    event = {}
    context = {}
    result = put_function(event, context)

    assert result['statusCode'] == 200

    body = json.loads(result['body'])
    expected_new_count = 1 
    assert body['count'] == expected_new_count

    table = dynamodb.Table(TEST_TABLE_NAME)
    response = table.get_item(Key={'ID': 'visit_count'})
    assert response['Item']['visit_count'] == expected_new_count
