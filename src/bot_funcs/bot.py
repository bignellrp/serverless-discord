from discord_webhook import DiscordWebhook, DiscordEmbed
from src.utils import dynamo_bot_funcs, discord_funcs, get_date, get_data, swap_players
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def get_top10(guild_id, body):
    """Get Top10 using player class"""
    try:
        webhook = DiscordWebhook(url=webhookurl)
        players = get_data.player()
        leaderboard = players.leaderboard()
        leaderboard = '\n'.join(str(score) 
                                + " | " 
                                + name for name,score 
                                        in leaderboard)
        # Embed Message
        embed=DiscordEmbed(
            title="Top10:",
            color='03b2f8'
        )
        embed.add_embed_field(name="Score | Player", 
                        value=leaderboard, inline=True)
        embed.set_thumbnail(url=f"{footyappurl}trophy.png")
        webhook.add_embed(embed)
        response = webhook.execute()

        return f'Can I help with anything else??'
            
    except Exception as e:
        logger.error(e)
        raise Exception(e)

def get_winpercentage(guild_id, body):
    """Lineup for both teams for this week"""
    try:
        webhook = DiscordWebhook(url=webhookurl)
        players = get_data.player()
        leaderboard = players.winpercentage()
        leaderboard = '\n'.join(str(score) 
                                + " | " 
                                + name for name,score 
                                        in leaderboard)
        # Embed Message
        embed=DiscordEmbed(
            title="Win Percentage:",
            color='03b2f8'
        )
        embed.add_embed_field(name="Score | Player", 
                        value=leaderboard, inline=True)
        embed.set_thumbnail(url=f"{footyappurl}percent.png")
        webhook.add_embed(embed)
        response = webhook.execute()

        return f'Can I help with anything else??'
            
    except Exception as e:
        logger.error(e)
        raise Exception(e)

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

def swap_player(guild_id, body):
        '''Swap player function'''
        options = body['data']['options'][0]['options']

        players = get_data.player()
        player_list = players.player_names()
        player_list = [pname[0] for pname in player_list]
        result = get_data.results()
        teama = result.teama()
        teamb = result.teamb()
        teams = teama + teamb

        for op in options:
            if op['name'] == 'curplayer':
                curplayer = op['value']
                if curplayer not in player_list:
                    raise Exception('Player not in the database!')
                elif curplayer not in teams:
                    raise Exception('Player not on the list for this week!')
            elif op['name'] == 'newplayer':
                newplayer = op['value']
                if curplayer not in player_list:
                    raise Exception('Player not in the database!')
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option.')
        
        if all([curplayer in teama, newplayer in teama]):
            raise Exception('Players are on the same team!')
        elif all([curplayer in teamb, newplayer in teamb]):
            raise Exception('Players are on the same team!')

        if newplayer not in teams:
            try: 
                message = swap_players.swap_player(curplayer, newplayer)
                return f'Swapped {curplayer} with {newplayer}.'
            except Exception as e:
                logger.error(e)
                raise Exception(e)
        else:
            try: 
                message = swap_players.swap_existing_player(curplayer, newplayer)
                return f'Swapped {curplayer} with {newplayer}.'
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

        ## Moved the update score function to a thread as the formulas took
        ## longer than 3 seconds and caused a discord error. This would
        ## need an extra step if the result was needed for the return.
        ## https://jun711.github.io/aws/aws-lambda-and-multi-threading-in-python/
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     executor.submit(dynamo_bot_funcs.update_score, scorea=scorea, scoreb=scoreb)
        # return f'Updated Score as TeamA: {scorea}, TeamB: {scoreb}'
        try: 
            message = dynamo_bot_funcs.update_score(scorea,scoreb)
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