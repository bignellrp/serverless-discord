from src.utils import dynamo_bot_funcs, discord_funcs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_teama(guild_id, body):
        """Players on Team A"""
        #file = discord.File("static/teama.png")
        #result = results()
        #teama = result.teama()
        #date = result.date()
        #scorea = result.scorea()
        #teama = "\n".join(item for item in teama)
        teama = "Joe,Bod,Rik,Amy,Emi"
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
            message = dynamo_bot_funcs.get_teama_dynamo(date)
            # print(message)
            return f'Team As score is {message}'
        except Exception as e:
            logger.error(e)
            raise Exception(e)