## Use this script to reset this weeks scores

from get_date import closest_wednesday
import boto3

player_table = boto3.resource('dynamodb').Table('player_table')
results_table = boto3.resource('dynamodb').Table('results_table')

results_table.update_item(
        Key={'Date': str(closest_wednesday)},
        UpdateExpression="set #1=:1, #2=:2",
        ExpressionAttributeNames={
            '#1': 'Team A Result?',
            '#2': 'Team B Result?'},
        ExpressionAttributeValues={
            ':1': '-',
            ':2': '-'},
        ReturnValues="UPDATED_NEW"
    )