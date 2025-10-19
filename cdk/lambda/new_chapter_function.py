import boto3
import uuid


def lambda_handler(event, context):
    CHAPTERS_TABLE_NAME = "Chapters"
    CHAPTERS_KEY_NAME = "ch-key"
    CHAPTERS_NUM_NAME = "ch-num"
    CHAPTERS_UID_NAME = "uid"

    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    dynamodb = boto3.resource("dynamodb")
    chapters_table = dynamodb.Table(CHAPTERS_TABLE_NAME)

    response = chapters_table.scan()
    items = response["Items"]

    while "LastEvaluatedKey" in response:
        response = chapters_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    max_num = 0
    if items:
        user_items = [item for item in items if item[CHAPTERS_UID_NAME] == user_id]
        if user_items:
            max_item = max(user_items, key=lambda x: int(x[CHAPTERS_NUM_NAME]))
            max_num = int(max_item[CHAPTERS_NUM_NAME])

    ch_num = max_num + 1

    ch_key = str(uuid.uuid4())

    chapters_table.put_item(
        Item={
            CHAPTERS_KEY_NAME: ch_key,
            CHAPTERS_NUM_NAME: ch_num,
            CHAPTERS_UID_NAME: user_id,
        }
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": {
            "ch-key": ch_key,
            "ch-num": ch_num
        }
    }
