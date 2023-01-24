from src.utils import dynamo_bot_funcs, discord_funcs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_teama_total(guild_id, body):
        """Players on Team A"""
        #file = discord.File("static/teama.png")
        #result = results()
        #teama = result.teama()
        #date = result.date()
        #scorea = result.scorea()
        #teama = "\n".join(item for item in teama)
        #teama = "Joe,Bod,Rik,Amy,Emi"
        #date = "2023-01-18"
        #scorea = "344"
        options = body['data']['options'][0]['options']
        #group_name = ''

        for op in options:
            if op['name'] == 'date':
                date = op['value']
            else:
                raise Exception(
                    f'{op["value"]} is not a valid option for get_teama.')
        # Embed Message
        #embed=discord.Embed(
        #    title="Date: " + date,
        #    color=discord.Color.green()
        #)
        #embed.add_field(name="Team A", value=teama, inline=True)
        #embed.set_thumbnail(url="attachment://teama.png")
        #embed.set_footer(text="Team A Score: "+str(scorea))
        #print("Posted Team A to discord!")
        try: 
            #await ctx.send(file=file, embed=embed)
            message = dynamo_bot_funcs.get_teama_total(date)
            # print(message)
            return f'Team As total is {message}'
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