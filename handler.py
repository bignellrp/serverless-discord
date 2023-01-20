##https://github.com/ker0olos/aws-lambda-discord-bot/blob/main/README.md

import json
import command_handler
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = 'e9955e14d08088e478ad1cb8785beb83ab31696fc74c2141cf4c85668de4f325'

def lambda_handler(event, context):
  try:
    body = json.loads(event['body'])
        
    signature = event['headers']['x-signature-ed25519']
    timestamp = event['headers']['x-signature-timestamp']

    # validate the interaction

    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    message = timestamp + json.dumps(body, separators=(',', ':'))
    
    try:
      verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
    except BadSignatureError:
      return {
        'statusCode': 401,
        'body': json.dumps('invalid request signature')
      }
    
    # handle the interaction

    t = body['type']

    if t == 1:
      return {
        'statusCode': 200,
        'body': json.dumps({
          'type': 1
        })
      }
    elif t == 2:
      return command_handler.command_handler(body)
    else:
      return {
        'statusCode': 400,
        'body': json.dumps('unhandled request type')
      }
  except:
    raise

