import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')

def get_teama_dynamo(date):
    try:
        response = dynamodb.get_item(
            Key={
                'Date': {'S': str(date)}
            },
            TableName='results_table',
        )
        if 'Item' not in response:
            raise Exception('Date Not Found')

        response = response['Item']['Team A Total']['N']

        return response
    except ClientError as e:
        raise Exception(f'Error getting score: {e}')