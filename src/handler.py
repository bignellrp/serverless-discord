import json
import logging
from re import sub
from src.utils import discord_funcs
from src.bot_funcs import bot

DISCORD_PING_PONG = {'statusCode': 200, 'body': json.dumps({"type": 1})}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

commands = {'fa': {'get_score': bot.get_teama_total, 
                   'update_scorea': bot.update_scorea, 
                   'update_score': bot.update_score, 
                   'add_player': bot.add_player,
                   'update_player': bot.update_player, 
                   'remove_player': bot.remove_player}}

def main(event, context):

    print(event)

    if not discord_funcs.valid_signature(event):
        return discord_funcs.discord_body(200, 2, 'Error Validating Discord Signature')

    body = json.loads(event['body'])

    if body['type'] == 1:
        return DISCORD_PING_PONG

    guild_id = body['guild_id']
    command = body['data']['name']
    sub_command = body['data']['options'][0]['name']

    try:
        bot_func = commands.get(command).get(sub_command)
        message = bot_func(guild_id, body)
        # return discord_funcs.discord_body(200, 3, message) #Interaction failure in discord
        return discord_funcs.discord_body(200, 4, message)
    except Exception as e:
        return discord_funcs.discord_body(200, 4, f'Unable to {sub_command}, {e}')
