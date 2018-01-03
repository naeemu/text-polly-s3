import boto3
import json
import logging
import urllib.parse
from contextlib import closing

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading function')
# dynamo = boto3.client('dynamodb')
polly = boto3.client('polly')
s3 = boto3.client('s3')
bucket = 'naeem-slack-api-lambda-polly-avs'

def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    slackEvent = urllib.parse.parse_qsl(event['body-json'])
    text = dict(slackEvent)['text']
    response = polly.synthesize_speech(
                    Text=text,
                    OutputFormat='mp3',
                    VoiceId='Emma',
                    TextType='text')
    with closing(response["AudioStream"]) as stream:
                s3.put_object(Key=context.aws_request_id + '.mp3', Body=stream.read(), Bucket=bucket)
    return "200 OK. Text: " + text
