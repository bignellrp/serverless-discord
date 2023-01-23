##############################################
# Run this script locally to add bot commands
##############################################
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
    "name": "lfg",
    "description": "Returns a specific group.",
    "options": [
        {
            "name": "create_group",
                    "description": "Create a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        },
                        {
                            "name": "size",
                            "description": "Size of the group.",
                            "type": 3,
                            "required": False
                        },
                        {
                            "name": "description",
                            "description": "Description for the group.",
                            "type": 3,
                            "required": False
                        }
                    ]
        },
        {
            "name": "join_group",
                    "description": "Join a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "leave_group",
                    "description": "Leave a group.",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "get_groups",
                    "description": "Get All groups",
                    "type": 1,
                    "options": [
                        {
                            "name": "avaliable",
                            "value": True,
                            "description": "If you want to only display groups wtih open spots.",
                            "type": 3,
                            "required": False
                        }
                    ]
        },
        {
            "name": "get_group",
                    "description": "Get a group",
                    "type": 1,
                    "options": [
                        {
                            "name": "name",
                            "description": "Name of the group.",
                            "type": 3,
                            "required": True
                        }
                    ]
        },
        {
            "name": "get_score",
                    "description": "get_score",
                    "type": 1,
                    "options": [
                        {
                            "name": "date",
                            "description": "Date we want",
                            "type": 3,
                            "required": True
                        }
                    ]
        }
    ]
}


response = requests.post(url, headers={
  "Authorization": f"Bot {DISCORD_TOKEN}"
}, json=json)

print(response.json())