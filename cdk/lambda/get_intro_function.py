import boto3
import json

CHAPTERS_KEY_NAME = "ch-key"
INTRO_TABLE_NAME = "Intro"
INTRO_CONTENT_NAME = "content"
INTRO_OPTIONS_NAME = "options"


def lambda_handler(event, context):
    print(event)
    query_params = event["queryStringParameters"]
    ch_key = query_params["ch-key"]

    dynamodb = boto3.resource("dynamodb")
    intro_table = dynamodb.Table(INTRO_TABLE_NAME)

    response = intro_table.scan()
    items = response["Items"]

    print(f"db items: {items}")

    while "LastEvaluatedKey" in response:
        response = intro_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    intro_body = {}
    for item in items:
        print(f"Item: {item}")
        if item[CHAPTERS_KEY_NAME] == ch_key:
            intro_body = {
                "content": item[INTRO_CONTENT_NAME],
                "options": item[INTRO_OPTIONS_NAME],
            }
            break

    print(f"intro body: {intro_body}")
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"body": intro_body}),
    }
