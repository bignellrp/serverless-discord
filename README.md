# Serverless Discord Slash Command Bot

This is a fully serverless Discord Bot that deploys using the serverless framework and runs in AWS Lambda without needing an API Gateway.
It uses slash commands to interact with an existing dynamodb table deployed as part of the Serverless Footy app.




# Prereq:
1. Install Footapp Web - This has the dynamodb tables needed
    Here is the Serverless Footy App code:
    https://github.com/bignellrp/serverless-footyapp
2. Create a Discord app with slash commands enabled
    This page helped me set up the discord bot:
    https://oozio.medium.com/serverless-discord-bot-55f95f26f743
    Note this page is old and the code needed tweaking so just
    follow the dicord setup part.
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
2. Add lambda layers, see instructions in the appendix for creating the layer zip
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

#Appendix

Discord Webhook is used for sending embeds. 
This requires an additional lambda layer.
Follow this guide for building the layer.
Make sure the machine used is Amazon Linux or Ubuntu and has 3.9 install.
I used a docker called 'ccmpbll/docker-diag-tools' locally to save on
building an ec2.

https://medium.com/@geoff.ford_33546/creating-a-pynacl-lambda-layer-c3f2e1b6ff11

Discord Webhook Commands found here: https://pypi.org/project/discord-webhook/