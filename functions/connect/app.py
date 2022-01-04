import os
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):

    connectionId: str = event['requestContext']['connectionId']
    apiKey: str = event['header']['apiKey']

    params: dict = {
        'TableName': os.environ['SOCKET_CONNECTIONS_TABLE_NAME'],
        'Item': {
            'connectionId': {
                'S': connectionId
            },
            'apiKey':{
                'S': apiKey
            }
        }
    }

    # Insert the connectionId of the connected device to the database
    dynamodb.put_item(**params)

    return None