from discord_webhook import DiscordWebhook, DiscordEmbed
from src.utils import dynamo_bot_funcs, discord_funcs, get_date
import logging
import os

#DISCORD_WEBHOOK_CHANNELID = os.environ.get('DISCORD_WEBHOOK_CHANNELID', '')
DISCORD_WEBHOOK_CHANNELID = '1068600560934191186' #Lambda finding the wrong channelID
DISCORD_WEBHOOK_TOKEN = os.environ.get('DISCORD_WEBHOOK_TOKEN', '')
FOOTYAPP_URL = os.environ.get('FOOTYAPP_URL', '')
webhookurl = f'https://discord.com/api/webhooks/{DISCORD_WEBHOOK_CHANNELID}/{DISCORD_WEBHOOK_TOKEN}'
footyappurl = f'{FOOTYAPP_URL}/static/'
print(webhookurl)
print(footyappurl)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_lineup(guild_id, body):
        """Lineup for both teams for this week"""
        try: 
            webhook = DiscordWebhook(url=webhookurl)
            webhook2 = DiscordWebhook(url=webhookurl)
            date = str(get_date.closest_wednesday)
            teama,teamb,scorea,scoreb,coloura,colourb = dynamo_bot_funcs.get_teams(date)
            teama = "\n".join(item for item in teama)
            teamb = "\n".join(item for item in teamb)
            
            ##Embed Message 1
            embed=DiscordEmbed(
                title="Date: " + date,
                color='03b2f8'
            )
            embed.add_embed_field(name="Team A", value=teama, inline=True)
            embed.set_thumbnail(url=f"{footyappurl}{coloura}.png")
            embed.set_footer(text="Team A Score: "+str(scorea))
            webhook.add_embed(embed)
            response = webhook.execute()

            ##Embed Message 2
            embed2=DiscordEmbed(
                title="Date: " + date,
                color='03b2f8'
            )
            embed2.add_embed_field(name="Team B", value=teamb, inline=True)
            embed2.set_thumbnail(url=f"{footyappurl}{colourb}.png")
            embed2.set_footer(text="Team B Score: "+str(scoreb))
            webhook2.add_embed(embed2)
            response = webhook2.execute()

            return f'Can I help with anything else??'
            
        except Exception as e:
            logger.error(e)
            raise Exception(e)

def update_scorea(guild_id, body):
        '''Function to update the result using 
        the values from the results page
        Takes in value to be added to the table updates item'''

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'scorea':
                score = op['value']
                try:
                    score = int(score)
                except:
                    input_type = type(score)
                    raise Exception(
                        f'Group size must be an integer, not {input_type}.')
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        try: 
            message = dynamo_bot_funcs.update_scorea(score)
            print(message)
            return f'Updated ScoreA with value: {score}'
        except Exception as e:
            logger.error(e)
            raise Exception(e)

def update_score(guild_id, body):
        '''Function to update the result using 
        the values from the results page
        Takes in value to be added to the table updates item'''

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'scorea':
                scorea = op['value']
                try:
                    scorea = int(scorea)
                except:
                    input_type = type(scorea)
                    raise Exception(
                        f'Group size must be an integer, not {input_type}.')
            elif op['name'] == 'scoreb':
                scoreb = op['value']
                try:
                    scoreb = int(scoreb)
                except:
                    input_type = type(scoreb)
                    raise Exception(
                        f'Group size must be an integer, not {input_type}.')
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        try: 
            message = dynamo_bot_funcs.update_score(scorea,scoreb)
            print(message)
            return f'Updated Score as TeamA: {scorea}, TeamB: {scoreb}'
        except Exception as e:
            logger.error(e)
            raise Exception(e)

def add_player(guild_id, body):
        '''Function to update the result using 
        the values from the results page
        Takes in value to be added to the table updates item'''

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'name':
                player = op['value']
            elif op['name'] == 'total':
                total = op['value']
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        try: 
            message = dynamo_bot_funcs.add_player(player,total)
            print(message)
            return f'Added {player} with total of: {total}'
        except Exception as e:
            logger.error(e)
            raise Exception(e)

def update_player(guild_id, body):
        '''Updates players total
        Takes in body from discord to update player'''

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'name':
                player = op['value']
            elif op['name'] == 'total':
                total = op['value']
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        try: 
            message = dynamo_bot_funcs.update_player(player,total)
            print(message)
            return f'Updated {player} with total of: {total}'
        except Exception as e:
            logger.error(e)
            raise Exception(e)

def remove_player(guild_id, body):
        '''Function to remove player from
        player table.
        Takes in body from discord with player name to remove'''

        options = body['data']['options'][0]['options']

        for op in options:
            if op['name'] == 'name':
                player = op['value']
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        try: 
            message = dynamo_bot_funcs.remove_player(player)
            print(message)
            return f'Removed {player}!'
        except Exception as e:
            logger.error(e)
            raise Exception(e)