import boto3
import json


def lambda_handler(event, context):
    QUESTIONS_TABLE_NAME = "Questions"
    QUESTIONS_ID_NAME = "question-id"
    QUESTIONS_ANSWER_NAME = "answer"

    INTRO_TABLE_NAME = "Intro"
    INTRO_KEY_NAME = "ch-key"
    INTRO_CONTENT_NAME = "content"
    INTRO_OPTIONS_NAME = "options"

    dynamodb = boto3.resource("dynamodb")

    # Create questions
    questions_table = dynamodb.Table(QUESTIONS_TABLE_NAME)

    questions = json.loads(event["body"]["questions"])
    for question_item in questions:
        questions_table.update_item(
            Key={
                QUESTIONS_ID_NAME: question_item["id"],
            },
            Item={QUESTIONS_ANSWER_NAME: question_item["answer"]},
        )

    # generate intro
    model_id = "amazon.nova-lite-v1:0"

    # Start a conversation with the user message.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    ai_intro_gen_query = f"""
        Pretend you are a storyteller writing a character, and you are inspired by some of your emotions you have 
        felt in the recent past, and in this very moment. You think about how you represented this character when 
        you recently left off writing 

            {} 

        Currently, to help inspire you to jump back into it, you write a short yes/no questionnaire for yourself 
        about how you were recently feeling: 

            {}

        Now you are ready. Inspired by your responses, write a short slice of life inspired snippet for a character. 
        Stay gender neutral, and focus on the character's inner thoughts. Try to achieve around a 400 word snippet. 
    """

    conversation = [
        {
            "role": "user",
            "content": [{"text": ai_intro_gen_query}],
        }
    ]

    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    generated_content = response["output"]["message"]["content"][0]["text"]

    body = json.loads(event["body"])
    intro_table = dynamodb.Table(INTRO_TABLE_NAME)
    intro_table.put_item(
        Item={
            INTRO_KEY_NAME: body["ch-key"],
            INTRO_CONTENT_NAME: generated_content,
            INTRO_OPTIONS_NAME: options_list,
        }
    )
