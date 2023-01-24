# Serverless Discord Slash Command Bot

This is a fully serverless Discord Bot that deploys using the serverless framework and runs in AWS Lambda without needing an API Gateway.
It uses slash commands to interact with an existing dynamodb table deployed as part of the Serverless Footy app.

https://github.com/bignellrp/serverless-footyapp


# Prereq:
1. Install Footapp Web - This has the dynamodb tables needed
2. Create a Discord app with slash commands enabled
3. Export the following variables locally

```
export DISCORD_CLIENT_ID=
export DISCORD_CLIENT_SECRET=
export DISCORD_PUBLIC_KEY=
export DISCORD_APPLICATION_ID=
export DISCORD_GUILD=
export DISCORD_TOKEN=
```

# Instructions:
1. Register commands 
```
python3 slash-commands/register_commands.py
```
2. Add lambda layer and upload pynacl_layer_3_9.zip with name nacl3_9 (Will add this to the serverless build at some point)
3. Install serverless iam
```
serverless plugin install -n serverless-iam-roles-per-function
```
4. Deploy App using Serverless
```
sls deploy
```
5. Add url outputted to Discord Interactions URL (Remove the / from the end first)
6. Test a command in discord

If you get a Interation Error or Exception check the lambda logs in CloudWatch