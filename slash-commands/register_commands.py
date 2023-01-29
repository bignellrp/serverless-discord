#######################################################
# Run this script locally to add or update bot commands
#######################################################

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

url = f'https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/guilds/{DISCORD_GUILD}/commands'

json = {
    "name": "fa",
    "description": "FootyAppCommands",
    "options": [
        {
            "name": "update_score",
                    "description": "Update score for Team A and B",
                    "type": 1,
                    "options": [
                        {
                            "name": "scorea",
                            "description": "Score for Team A",
                            "type": 3,
                            "required": True
                        },
                        {
                            "name": "scoreb",
                            "description": "Score for Team B",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "add_player",
                    "description": "Add a new player.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the player.",
                            "type": 3,
                            "required": True
                        },
                        {
                            "name": "total",
                            "description": "Players Total",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "update_player",
                    "description": "Update a players total.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the player.",
                            "type": 3,
                            "required": True
                        },
                        {
                            "name": "total",
                            "description": "Players Total",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "remove_player",
                    "description": "Remove a player.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the player.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "get_lineup",
                    "description": "Get Lineup for this week",
                    "type": 1
        }
    ]
}


response = requests.post(url, headers={
  "Authorization": f"Bot {DISCORD_TOKEN}"
}, json=json)

print(response.json())