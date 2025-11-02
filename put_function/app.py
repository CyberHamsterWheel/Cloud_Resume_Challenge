import json
import boto3

# import requests

session = boto3.Session()
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('resume-website-visitor-counter')

def put_function(event, context):
    response = table.get_item(Key={'ID': 'visit_count'})
    if 'Item' in response:
        current_count = response['Item'].get('visit_count', 0)
    else:
        current_count = 0
        table.put_item(Item={'ID': 'visit_count',
                             'visit_count': current_count})
        
    new_count = current_count + 1
    table.update_item(
        Key={
            'ID': 'visit_count'
        },
        UpdateExpression='SET visit_count = :val1',
        ExpressionAttributeValues={
            ':val1': new_count
        },
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://iohannah.com',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
        },
        'body': json.dumps({ 'count': int(new_count) })
    }



"""Sample pure Lambda function

Parameters
----------
event: dict, required
    API Gateway Lambda Proxy Input Format

    Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

context: object, required
    Lambda Context runtime methods and attributes

    Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

Returns
------
API Gateway Lambda Proxy Output Format: dict

    Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
"""

