import boto3
from botocore.exceptions import ClientError
from src.utils import get_date, post_stats

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')
player_table = boto3.resource('dynamodb').Table('player_table')

def get_teams(date):
    try:
        print(f"Getting teams for date: {date}")
        response = dynamodb.get_item(
            Key={
                'Date': {'S': str(date)}
            },
            TableName='results_table',
        )
        if 'Item' not in response:
            raise Exception('Date Not Found')

        teama = []
        teama.append(response['Item']['Team A Player 1']['S'])
        teama.append(response['Item']['Team A Player 2']['S'])
        teama.append(response['Item']['Team A Player 3']['S'])
        teama.append(response['Item']['Team A Player 4']['S'])
        teama.append(response['Item']['Team A Player 5']['S'])
        teamb = []
        teamb.append(response['Item']['Team B Player 1']['S'])
        teamb.append(response['Item']['Team B Player 2']['S'])
        teamb.append(response['Item']['Team B Player 3']['S'])
        teamb.append(response['Item']['Team B Player 4']['S'])
        teamb.append(response['Item']['Team B Player 5']['S'])
        
        print("Can give error N or S if total field type is wrong")
        scorea = response['Item']['Team A Total']['N']
        scoreb = response['Item']['Team B Total']['N']

        coloura = response['Item']['Team A Colour']['S']
        colourb = response['Item']['Team B Colour']['S']

        return teama,teamb,scorea,scoreb,coloura,colourb
    except ClientError as e:
        raise Exception(f'Error getting values: {e}')

def get_teama(date):
    try:
        print(f"Getting teama for date: {date}")
        response = dynamodb.get_item(
            Key={
                'Date': {'S': str(date)}
            },
            TableName='results_table',
        )
        if 'Item' not in response:
            raise Exception('Date Not Found')

        teama = []
        teama.append(response['Item']['Team A Player 1']['S'])
        teama.append(response['Item']['Team A Player 2']['S'])
        teama.append(response['Item']['Team A Player 3']['S'])
        teama.append(response['Item']['Team A Player 4']['S'])
        teama.append(response['Item']['Team A Player 5']['S'])

        scorea = response['Item']['Team A Total']['N']

        return teama,scorea
    except ClientError as e:
        raise Exception(f'Error getting values: {e}')

def get_teamb(date):
    try:
        print(f"Getting teamb for date: {date}")
        response = dynamodb.get_item(
            Key={
                'Date': {'S': str(date)}
            },
            TableName='results_table',
        )
        if 'Item' not in response:
            raise Exception('Date Not Found')

        teamb = []
        teamb.append(response['Item']['Team B Player 1']['S'])
        teamb.append(response['Item']['Team B Player 2']['S'])
        teamb.append(response['Item']['Team B Player 3']['S'])
        teamb.append(response['Item']['Team B Player 4']['S'])
        teamb.append(response['Item']['Team B Player 5']['S'])

        scoreb = response['Item']['Team B Total']['N']

        return teamb,scoreb
    except ClientError as e:
        raise Exception(f'Error getting values: {e}')

def update_score(scorea,scoreb):
    '''Adds score to results table
    if Date is last wednesday and
    Team A Result = '-' '''
    try:
        date = str(get_date.closest_wednesday)
        print(f"Adding scores: {scorea} and {scoreb} for {date}")
        results_table.update_item(
            Key={'Date': date},
            UpdateExpression="set #1=:1, #2=:2",
            ConditionExpression="#1=:3",
            ExpressionAttributeNames={
                '#1': 'Team A Result?',
                '#2': 'Team B Result?'},
            ExpressionAttributeValues={
                ':1': scorea,
                ':2': scoreb,
                ':3': '-'},
            ReturnValues="UPDATED_NEW"
        )
        response = post_stats.update_formulas()
    except ClientError as e:
        raise Exception(f'Error adding score: {e}')

def add_player(player,total):
    '''Adds player to player table'''
    try:
        print(f"Adding {player} with score {total}")
        player_table.put_item(
            Item={
                'Name': player,
                'Total': total,
                'Wins': '0',
                'Draws': '0',
                'Losses': '0',
                'Score': '0',
                'Playing': 'o',
                'Played': '0',
                'Percent Calc': '0',
                'Win Percentage': '0'
            }
        )
    except ClientError as e:
        raise Exception(f'Error adding player: {e}')
    return

def update_player(player,total):
    '''Updates players total'''
    try:
        print(f"Updating {player} with score {total}")
        player_table.update_item(
            Key={'Name': player},
            UpdateExpression="set #t=:t",
            ExpressionAttributeNames={
                '#t': 'Total'},
            ExpressionAttributeValues={
                ':t': total},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error updating player: {e}')

def remove_player(player):
    '''Deletes player from player table'''
    try:
        print(f"Removing {player}")
        player_table.delete_item(
            Key={'Name': player}
        )
    except ClientError as e:
        raise Exception(f'Error removing player: {e}')
    return