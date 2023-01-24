import boto3
from botocore.exceptions import ClientError
from src.utils import get_date

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')

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

def update_scorea(value):
    try:
        results_table.update_item(   
            Key={'Date': get_date.next_wednesday},
            UpdateExpression="set #1=:1",
            ExpressionAttributeNames={
                '#1': 'Team A Result?'},
            ExpressionAttributeValues={
                ':1': value},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error adding score: {e}')