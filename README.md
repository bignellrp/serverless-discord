Serverless Discord Slash Command Bot

Prereq:
1. Install Footapp Web - This has the dynamodb tables needed
2. Create a Discord app with slash commands enabled
3. Export the following variables locally

export DISCORD_CLIENT_ID=
export DISCORD_CLIENT_SECRET=
export DISCORD_PUBLIC_KEY=
export DISCORD_APPLICATION_ID=
export DISCORD_GUILD=
export DISCORD_TOKEN=

Instructions:
1. Run python3 slash-commands/register_commands.py
2. Add lambda layer and upload pynacl_layer_3_9.zip with name nacl3_9 (Will add this to the serverless build at some point)
3. Install serverless iam - serverless plugin install -n serverless-iam-roles-per-function
4. sls deploy
5. Add url outputted to Discord Interactions URL (Remove the / from the end first)
6. Test a command in discord

If you get a Interation Error or Exception check the lambda logs in CloudWatch