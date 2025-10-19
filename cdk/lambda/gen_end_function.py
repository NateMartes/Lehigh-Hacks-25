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
    return f"""You are writing a therapeutic storytelling exercise. This is a continuation of a character-driven narrative.

    PREVIOUS STORY SEGMENT:
    {intro_item[INTRO_CONTENT_NAME]}

    CHOICES THAT WERE OFFERED:
    1. {intro_item[INTRO_OPTIONS_NAME][0]}
    2. {intro_item[INTRO_OPTIONS_NAME][1]}
    3. {intro_item[INTRO_OPTIONS_NAME][2]}

    THE CHOICE MADE:
    {choice}

    YOUR TASK:
    Write a 300-400 word continuation that:
    - Shows the immediate consequence of this choice
    - Focuses on the character's internal emotional response and thoughts
    - Uses gender-neutral language (they/them pronouns)
    - Ends with a reflective moment that invites the reader to consider their own feelings
    - Uses a compassionate, introspective tone suitable for therapeutic self-reflection
    - Concludes the story arc with emotional resolution or insight

    Write the continuation now:"""


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
