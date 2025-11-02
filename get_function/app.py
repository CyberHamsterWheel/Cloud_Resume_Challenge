import json
import boto3


# import requests
def get_function(event, context):
    session = boto3.Session()
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table('resume-website-visitor-counter')
    response = table.get_item(Key={'ID': 'visit_count'})
    visitors_count = response.get('Item', {}).get('visit_count', 0)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://iohannah.com',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({ 'count': int(visitors_count) })
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



