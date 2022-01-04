import json
import boto3
import logging
import os


dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    message = body['payload']
    apiKey = body['apiKey']
    

    apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', 
        endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])
    
    connectionIds = get_connected_users_by_api_key(apiKey=apiKey)
    # Send message to all connected user with apiKey 
    for connectionId in connectionIds:
        apigatewaymanagementapi.post_to_connection(
            Data=message,
            ConnectionId=connectionId['connectionId']
        )

    return None

def get_connected_users_by_api_key(apiKey):
    try:
        data: dict = dynamodb.Table('nursesimple-agents-stats').query(
                KeyConditionExpression='apiKey = :apk',
                ExpressionAttributeValues={
                    ':apk': apiKey
                })
        if 'Items' in data:
            return data['Items']
        return None
    except:
        logging.exception(' ')