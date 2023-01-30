from src.utils import dynamo_bot_funcs, discord_funcs, get_date, calc_stats
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')
results_table = boto3.resource('dynamodb').Table('results_table')
player_table = boto3.resource('dynamodb').Table('player_table')

def update_formulas():
    '''Updates formulas'''
    date = str(get_date.closest_wednesday)
    teama,teamb,scorea,scoreb,coloura,colourb = dynamo_bot_funcs.get_teams(date)
    played_thisweek = teama + teamb
    for name in played_thisweek:
        calc = calc_stats.calc_wdl(name)
        wins = calc[0]
        draws = calc[1]
        losses = calc[2]
        score = int(wins) * 3 + int(draws)
        played = int(wins) + int(draws) + int(losses)
        percentage = int(wins) / int(played) * 100
        percentage = int(percentage)
        if int(wins) < 5:
            winpercentage = '0'
        else:
            winpercentage = percentage
        try:
            player_table.update_item(
                Key={'Name': name},
                UpdateExpression="set Wins=:w, Draws=:d, Losses=:l, Score=:s, Played=:p, #pc=:pc, #wp=:wp",
                ExpressionAttributeNames={
                    '#pc': 'Percent Calc',
                    '#wp': 'Win Percentage'},
                ExpressionAttributeValues={
                    ':w': wins,
                    ':d': draws,
                    ':l': losses,
                    ':s': score,
                    ':p': played,
                    ':pc': percentage,
                    ':wp': winpercentage},
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            raise Exception(f'Error updating values: {e}')
    return