import boto3
from botocore.exceptions import ClientError
from src.utils import get_date

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')
player_table = boto3.resource('dynamodb').Table('player_table')

def get_teama_total(date):
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

def update_score(scorea,scoreb):
    try:
        results_table.update_item(   
            Key={'Date': get_date.next_wednesday},
            UpdateExpression="set #1=:1, #2=:2",
            ExpressionAttributeNames={
                '#1': 'Team A Result?',
                '#2': 'Team B Result?'},
            ExpressionAttributeValues={
                ':1': scorea,
                ':2': scoreb},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error adding score: {e}')

def add_player(player,total):
    '''Adds player to player table'''
    try:
        player_table.update_item(
            Key={'Name': player},
            UpdateExpression="set #n=:n, #t=:t, #w=:w, #d=:d, #l=:l, #s=:s, #p=:p, #pc=:pc, #wp=:wp",
            ExpressionAttributeNames={
                '#n': 'Name', #Name was a reserved attribute
                '#t': 'Total',
                '#w': 'Wins',
                '#d': 'Draws',
                '#l': 'Losses',
                '#s': 'Score',
                '#p': 'Played',
                '#pc': 'Percent Calc',
                '#wp': 'Win Percentage'},
            ExpressionAttributeValues={
                ':n': player,
                ':t': total,
                ':w': '0',
                ':d': '0',
                ':l': '0',
                ':s': '0',
                ':p': '0',
                ':pc': '0',
                ':wp': '0'},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error adding player: {e}')

def update_player(player,total):
    '''Updates players total'''
    try:
        player_table.update_item(
            Key={'Name': player},
            UpdateExpression="set #n=:n, #t=:t",
            ExpressionAttributeNames={
                '#n': 'Name',
                '#t': 'Total'},
            ExpressionAttributeValues={
                ':n': player,
                ':t': total},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error updating player: {e}')

def remove_player(player):
    '''Deletes player from player table'''
    try:
        player_table.delete_item(
            Key={'Name': player}
        )
    except ClientError as e:
        raise Exception(f'Error removing player: {e}')
    return