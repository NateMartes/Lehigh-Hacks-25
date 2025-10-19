import boto3
import json

CHAPTERS_TABLE_NAME = "Chapters"
CHAPTERS_KEY_NAME = "ch-key"
CHAPTERS_NUM_NAME = "ch-num"
CHAPTERS_UID_NAME = "uid"

def lambda_handler(event, context):
    query_params = event["queryStringParameters"]
    uid = query_params["uid"]

    dynamodb = boto3.resource("dynamodb")
    chapter_table = dynamodb.Table(CHAPTERS_TABLE_NAME)

    response = chapter_table.scan()
    items = response["Items"]

    while "LastEvaluatedKey" in response:
        response = chapter_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    chapters = []
    for item in items:
        if item[CHAPTERS_UID_NAME] == uid:
            chapters.append({
                    "ch-key": item[CHAPTERS_KEY_NAME],
                    "ch-num": int(item[CHAPTERS_NUM_NAME])
            })

    chapters = sorted(chapters, key=lambda item: item["ch-num"])

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"chapters": chapters})
    }