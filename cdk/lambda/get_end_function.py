import boto3
import json

END_TABLE_NAME = "End"
CHAPTERS_KEY_NAME = "ch-key"
END_CONTENT_NAME = "content"
END_OPTIONS_NAME = "options"


def lambda_handler(event, context):
    query_params = event["queryStringParameters"]
    ch_key = query_params["ch-key"]

    dynamodb = boto3.resource("dynamodb")
    end_table = dynamodb.Table(END_TABLE_NAME)

    response = end_table.scan()
    items = response["Items"]

    while "LastEvaluatedKey" in response:
        response = end_table.scan = end_table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response["Items"])

    end_content = {}
    for item in items:
        if item[CHAPTERS_KEY_NAME] == ch_key:
            end_content = {
                "end_content": item[END_CONTENT_NAME],
                "option_selected": item[END_OPTIONS_NAME],
            }
            break

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"body": end_content}),
    }
