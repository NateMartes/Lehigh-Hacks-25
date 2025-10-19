import base64
import boto3
import json

VOICE_ID = "Salli"
VOICE_ENGINE = "generative"

def lambda_handler(event, context):
    body = json.loads(event["body"])

    text = body["text"]
    
    polly = boto3.client("polly")

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=VOICE_ID,
        Engine=VOICE_ENGINE
    )

    audio_stream = response["AudioStream"].read()

    audio_base64 = base64.b64encode(audio_stream).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "audio-base64": audio_base64,
            "content-type": response["ContentType"]
        })
    }