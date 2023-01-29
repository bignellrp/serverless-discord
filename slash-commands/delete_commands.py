################################################
# Run this script locally to delete bot commands
################################################

# Updating and Deleting a Command
# Commands can be deleted and updated by making DELETE and PATCH calls to the command endpoint. Those endpoints are

# applications/<my_application_id>/commands/<command_id> for global commands, or
# applications/<my_application_id>/guilds/<guild_id>/commands/<command_id> for guild commands
# Because commands have unique names within a type and scope, we treat POST requests for new commands as upserts. 
# That means making a new command with an already-used name for your application will update the existing command.

import requests
import os

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")
DISCORD_APPLICATION_ID = os.environ.get("DISCORD_APPLICATION_ID")
DISCORD_GUILD = os.environ.get("DISCORD_GUILD")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

commandid = '1064213321160593540'

deleteurl = f'https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/guilds/{DISCORD_GUILD}/commands/{commandid}'

response = requests.delete(deleteurl, headers={
  "Authorization": f"Bot {DISCORD_TOKEN}"})