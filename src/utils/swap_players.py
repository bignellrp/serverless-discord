from src.utils.get_date import next_wednesday
from src.utils.get_data import player,results
import boto3
from botocore.exceptions import ClientError

player_table = boto3.resource('dynamodb').Table('player_table')
results_table = boto3.resource('dynamodb').Table('results_table')
dynamodb = boto3.client('dynamodb')
player_class = player()
result = results()

def swap_player(player_current,player_new):
    '''Takes in a list of two players
    finds their score and swaps them 
    in the results table'''
    all_players = player_class.all_players()
    for name, total in all_players:
        if name == player_current:
            player_current_score = total

    for name, total in all_players:
        if name == player_new:
            player_new_score = total

    ##Work out difference between player scores
    player_score_difference = int(player_current_score) \
                                  - int(player_new_score)
    
    ta = result.teama()
    tb = result.teamb()
    tta = result.totala()
    ttb = result.totalb()
    if player_current in tb : 
        team = "B"
        team_result = ttb
        index = tb
    else:
        team = "A"
        team_result = tta
        index = ta

    ##Find index of player in team
    index = index.index(player_current)
    index = int(index) + 1

    ##Find the score from Team A or B
    col_result_num = f'Team {team} Total'
    col_player = f'Team {team} Player {index}'

    ##New Result is current result minus difference
    new_result = int(team_result) - player_score_difference 

    ##Update values with new player and new score,
    ##using date as the key
    try:
        results_table.update_item(
            Key={'Date': str(next_wednesday)},
            UpdateExpression="set #1=:1, #2=:2",
            ConditionExpression="#3=:3",
            ExpressionAttributeNames={
                '#1': col_result_num,
                '#2': col_player,
                '#3': 'Team A Result?'},
            ExpressionAttributeValues={
                ':1': new_result,
                ':2': player_new,
                ':3': '-'},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error swapping players: {e}')
    return

def swap_existing_player(player_current,player_new):
    '''Takes in a list of two players
    finds their score and swaps them 
    in the results table if players
    are both playing'''

    players = player_class.all_players()
    for name, total in players:
        if name == player_current:
            player_current_score = total

    for name, total in players:
        if name == player_new:
            player_new_score = total

    ##Work out difference between player scores
    player_score_difference = int(player_current_score) \
                                  - int(player_new_score)
    ta = result.teama()
    tb = result.teamb()
    if player_current in tb : 
        team_curr = "B"
        team_new = "A"
        current_index = tb
        new_index = ta
    else:
        team_curr = "A"
        team_new = "B"
        current_index = ta
        new_index = tb

    ##Find index of player in team
    current_index = current_index.index(player_current)
    current_index = int(current_index) + 1
    new_index = new_index.index(player_new)
    new_index = int(new_index) + 1

    ##Constructing the Attribute Name
    curr_player = f'Team {team_curr} Player {current_index}'
    new_player = f'Team {team_new} Player {new_index}'

    ##New Result is current result minus difference
    tota = result.totala()
    new_result_a = int(tota) - player_score_difference

    ##New Result is current result minus difference
    totb = result.totalb()
    new_result_b = int(totb) - player_score_difference

    ##Update values with new player and new score,
    ##using date as the key
    ##and with curr player swapped with new player

    try:
        results_table.update_item(
            Key={'Date': str(next_wednesday)},
            UpdateExpression="set #1=:1, #2=:2, #4=:4, #5=:5",
            ConditionExpression="#3=:3",
            ExpressionAttributeNames={
                '#1': 'Team A Total',
                '#2': 'Team B Total',
                '#3': 'Team A Result?',
                '#4': curr_player,
                '#5': new_player},
            ExpressionAttributeValues={
                ':1': new_result_a,
                ':2': new_result_b,
                ':3': '-',
                ':4': player_new,
                ':5': player_current},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        raise Exception(f'Error swapping players: {e}')
    return