import boto3
import json
import uuid

CHAPTERS_TABLE_NAME = "Chapters"
CHAPTERS_KEY_NAME = "ch-key"
CHAPTERS_NUM_NAME = "ch-num"
CHAPTERS_UID_NAME = "uid"
    
END_TABLE_NAME = "End"
END_CHOICE_NAME = "choice"
END_CONTENT_NAME = "content"

QUESTIONS_TABLE_NAME = "Questions"
QUESTIONS_ID_NAME = "question-id"
QUESTIONS_CONTENT_NAME = "content"
QUESTIONS_ANSWER_NAME = "answer"

MODEL_ID = "amazon.nova-lite-v1:0"

def gen_prompt(prev_end):
    if not prev_end:
        return """
            You are a therapist trying to understand your patient's situation.
            You also write stories to help your patient be aware of their actions and
            reframe their thoughts. Please generate five True or False questions to survey 
            your patient and write a story. Please separate each question with the | symbol. 
            Do not write anything else but the questions.
        """

    return f"""
        You are a therapist trying to understand your patient's situation.
        You also write stories to help your patient be aware of their actions and
        reframe their thoughts. Please generate five True or False questions to survey your patient
        and write a story. The questions can inquire about what has been done
        since the last story. Here is the action the patient chose in the last story:
        {prev_end[END_CHOICE_NAME]}. Here is how the last story ended:
        {prev_end[END_CONTENT_NAME]}. Please separate each question with the | symbol.
        Do not write anything else but the questions.
    """

def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    body = json.loads(event["body"])
    
    ch_key = body["ch-key"]

    dynamodb = boto3.resource("dynamodb")
    chapters_table = dynamodb.Table(CHAPTERS_TABLE_NAME)
    end_table = dynamodb.Table(END_TABLE_NAME)
    questions_table = dynamodb.Table(QUESTIONS_TABLE_NAME)

    ch_response = chapters_table.scan()
    ch_items = ch_response["Items"]
    
    while "LastEvaluatedKey" in ch_response:
        ch_response = chapters_table.scan(ExclusiveStartKey=ch_response["LastEvaluatedKey"])
        ch_items.extend(ch_response["Items"])

    prev_ch_key = ""
    if ch_items:
        user_items = [item for item in ch_items if item[CHAPTERS_UID_NAME] == user_id]
        if user_items:
            prev_item = max(user_items, key=lambda x: int(x[CHAPTERS_NUM_NAME]))
            user_items.remove(prev_item)
            prev_item = max(user_items, key=lambda x: int(x[CHAPTERS_NUM_NAME]))
            if prev_item:
                prev_ch_key = prev_item[CHAPTERS_KEY_NAME]

    prev_end = {}
    if prev_ch_key:
        end_response = end_table.scan()
        end_items = end_response["Items"]

        while "LastEvaluatedKey" in end_response:
            end_response = end_table.scan(ExclusiveStartKey=end_response["LastEvaluatedKey"])
            end_items.extend(end_response["Items"])

        prev_end = [item for item in end_items if item[CHAPTERS_KEY_NAME] == prev_ch_key][0]

    prompt = gen_prompt(prev_end)

    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]
    
    ai_response = client.converse(
        modelId=MODEL_ID,
        messages=conversation,
        inferenceConfig={"temperature": 0.5, "topP": 0.9}
    )
    ai_response_text = ai_response["output"]["message"]["content"][0]["text"]
    
    questions = ai_response_text.split('|')
    questions_ids = [str(uuid.uuid4()) for q in questions]

    for i in range(len(questions)):
        questions_table.put_item(
            Item={
                CHAPTERS_KEY_NAME: ch_key,
                QUESTIONS_ID_NAME: questions_ids[i],
                QUESTIONS_CONTENT_NAME: questions[i],
                QUESTIONS_ANSWER_NAME: None
            }
        )
    
    return {
        "statusCode": 200,
    }