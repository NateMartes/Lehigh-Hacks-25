import boto3
import uuid

def lambda_handler(event, context):
    CHAPTERS_TABLE_NAME = "Chapters"

    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    dynamodb = boto3.resource("dynamodb")
    chapters_table = dynamodb.Table(CHAPTERS_TABLE_NAME)

    ch_key = str(uuid.uuid4())

    chapters_table.put_item(
        Item={
            "ch-key": ch_key,
            "uid": user_id
        }
    )

    return {
        "statusCode": 200,
        "ch-key": ch_key
    }
