import boto3
import json

END_TABLE_NAME = "End"
END_CHOICE_NAME = "choice"
END_CONTENT_NAME = "content"

QUESTIONS_TABLE_NAME = "Questions"
QUESTIONS_ID_NAME = "question-id"
QUESTIONS_ANSWER_NAME = "answer"

INTRO_TABLE_NAME = "Intro"
INTRO_KEY_NAME = "ch-key"
INTRO_CONTENT_NAME = "content"
INTRO_OPTIONS_NAME = "options"

CHAPTERS_TABLE_NAME = "Chapters"
CHAPTERS_KEY_NAME = "ch-key"
CHAPTERS_NUM_NAME = "ch-num"
CHAPTERS_UID_NAME = "uid"

MODEL_ID = "amazon.nova-lite-v1:0"


def get_prev_chapter_end(user_id):
    dynamodb = boto3.resource("dynamodb")
    chapters_table = dynamodb.Table(CHAPTERS_TABLE_NAME)

    ch_response = chapters_table.scan()
    ch_items = ch_response["Items"]

    while "LastEvaluatedKey" in ch_response:
        ch_response = chapters_table.scan(
            ExclusiveStartKey=ch_response["LastEvaluatedKey"]
        )
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
        dynamodb = boto3.resource("dynamodb")
        end_table = dynamodb.Table(END_TABLE_NAME)
        end_response = end_table.scan()
        end_items = end_response["Items"]

        while "LastEvaluatedKey" in end_response:
            end_response = end_table.scan(
                ExclusiveStartKey=end_response["LastEvaluatedKey"]
            )
            end_items.extend(end_response["Items"])

        prev_end = [
            item for item in end_items if item[CHAPTERS_KEY_NAME] == prev_ch_key
        ][0]

    return prev_end


def get_qnas(questions):
    qnas = {}
    dynamodb = boto3.resource("dynamodb")
    questions_table = dynamodb.Table(QUESTIONS_TABLE_NAME)
    for question_item in questions:
        question = questions_table.get_item(
            Key={QUESTIONS_ID_NAME: question_item["id"]}
        )

        qnas[question["content"]] = question["answer"]

    return qnas


def lambda_handler(event, context):
    user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    dynamodb = boto3.resource("dynamodb")
    # Create questions
    questions_table = dynamodb.Table(QUESTIONS_TABLE_NAME)

    questions = json.loads(event["body"])["questions"]
    for question_item in questions:
        questions_table.update_item(
            Key={
                QUESTIONS_ID_NAME: question_item["question-id"],
            },
            Item={QUESTIONS_ANSWER_NAME: question_item["answer"]},
        )

    previous_ending = get_prev_chapter_end(user_id)
    print(previous_ending)

    questionnaire = get_qnas(questions)
    print(questionnaire)

    # Start a conversation with the user message.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    ai_intro_gen_query = f"""
        Pretend you are a storyteller writing a character, and you are inspired by some of your emotions you have 
        felt in the recent past, and in this very moment. You think about how you represented this character when 
        you recently left off writing 

            {previous_ending} 

        Currently, to help inspire you to jump back into it, you write a short yes/no questionnaire for yourself 
        about how you were recently feeling: 

            {questionnaire}

        Now you are ready. Inspired by your responses, write a short slice of life inspired snippet for a character. 
        Stay gender neutral, and focus on the character's inner thoughts. Try to achieve around a 400 word snippet. 
        End the snippet with a decision to make, and give 3 choices for the reader to make. Partition your response using vertical bars like so:
        story || question1 || question2 || question3. do not label your sections or questions 
    """

    conversation = [
        {
            "role": "user",
            "content": [{"text": ai_intro_gen_query}],
        }
    ]

    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=MODEL_ID,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    generated_content = response["output"]["message"]["content"][0]["text"]

    content = generated_content.split("||")[0]
    option1 = generated_content.split("||")[1]
    option2 = generated_content.split("||")[2]
    option3 = generated_content.split("||")[3]

    options_list = [option1, option2, option3]

    body = json.loads(event["body"])
    intro_table = dynamodb.Table(INTRO_TABLE_NAME)
    intro_table.put_item(
        Item={
            INTRO_KEY_NAME: body["ch-key"],
            INTRO_CONTENT_NAME: generated_content,
            INTRO_OPTIONS_NAME: options_list,
        }
    )

    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}}
