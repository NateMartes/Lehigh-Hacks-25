import boto3
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    chapters_table = dynamodb.Table("Chapters")
    
    key = str(uuid.uuid4())
    
    chapters_table.put_item(
        Item={
            "ch-key": key,
            "uid": "John Doe"
        }
    )

    return {
        "statusCode": 200,
        "body": "Success"
    }