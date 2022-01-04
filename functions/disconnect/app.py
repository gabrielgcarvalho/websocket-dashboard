import boto3
import os

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']

    # Delete connectionId from the database
    params: dict = {
        'TableName': os.environ['SOCKET_CONNECTIONS_TABLE_NAME'],
        'Key': {
            'connectionId': {
                'S': connectionId
                }
            }
        }

    dynamodb.delete_item(**params)

    return {}