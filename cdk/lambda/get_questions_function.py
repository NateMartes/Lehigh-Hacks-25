import boto3

def lambda_handler(event, context):
    QUESTIONS_TABLE_NAME = "Questions"
    CHAPTERS_KEY_NAME = "ch-key"
    QUESTIONS_ID_NAME = "question-id"
    QUESTIONS_CONTENT_NAME = "content"
    
    query_params = event["queryStringParameters"]
    ch_key = query_params["ch-key"]

    dynamodb = boto3.resource("dynamodb")
    questions_table = dynamodb.Table(QUESTIONS_TABLE_NAME)

    response = questions_table.scan()
    items = response["Items"]
    
    while "LastEvaluatedKey" in response:
        response = questions_table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    questions = []
    for item in items:
        if item[CHAPTERS_KEY_NAME] == ch_key:
            questions.append(
                {
                    "question-id": item[QUESTIONS_ID_NAME],
                    "content": item[QUESTIONS_CONTENT_NAME]
                }
            )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": {
            "questions": questions
        }
    }