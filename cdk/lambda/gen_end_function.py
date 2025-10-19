import boto3
import json

CHAPTERS_KEY_NAME = "ch-key"

INTRO_TABLE_NAME = "Intro"
INTRO_CONTENT_NAME = "content"
INTRO_OPTIONS_NAME = "options"

END_TABLE_NAME = "End"
END_CHOICE_NAME = "choice"
END_CONTENT_NAME = "content"

MODEL_ID = "amazon.nova-lite-v1:0"


def gen_prompt(intro_item, choice):
    return f"""
        Pretend you are a storyteller writing a character, and you are inspired by some of your emotions you have 
        felt in the recent past. You had started a choose-your-own-adventure story like this:
        
        {intro_item[INTRO_CONTENT_NAME]}

        You then provided the following options:

        {intro_item[INTRO_OPTIONS_NAME]}

        The following choice was selected:

        {choice}

        Now you are ready. Inspired by the choice made, end the story with possibility for reflection. 
        Stay gender neutral, and focus on the character's inner thoughts. Give no more than a 400 word snippet.
    """


def lambda_handler(event, context):
    body = json.loads(event["body"])

    ch_key = body["ch-key"]
    choice = body["choice"]

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    dynamodb = boto3.resource("dynamodb")

    intro_table = dynamodb.Table(INTRO_TABLE_NAME)
    end_table = dynamodb.Table(END_TABLE_NAME)

    intro_response = intro_table.scan()
    intro_items = intro_response["Items"]

    while "LastEvaluatedKey" in intro_response:
        intro_response = intro_table.scan(
            ExclusiveStartKey=intro_response["LastEvaluatedKey"]
        )
        intro_items.extend(intro_response["Items"])

    ch_intro = None
    for item in intro_items:
        if item[CHAPTERS_KEY_NAME] == ch_key:
            ch_intro = item
            break

    prompt = gen_prompt(ch_intro, choice)

    conversation = [{"role": "user", "content": [{"text": prompt}]}]

    ai_response = client.converse(
        modelId=MODEL_ID,
        messages=conversation,
        inferenceConfig={"temperature": 0.5, "topP": 0.9},
    )
    story_end = ai_response["output"]["message"]["content"][0]["text"]

    end_table.put_item(
        Item={
            CHAPTERS_KEY_NAME: ch_key,
            END_CHOICE_NAME: choice,
            END_CONTENT_NAME: story_end,
        }
    )

    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}}

