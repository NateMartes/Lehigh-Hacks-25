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

MODEL_ID = "us.meta.llama3-3-70b-instruct-v1:0"


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
            if user_items:
                prev_item = max(user_items, key=lambda x: int(x[CHAPTERS_NUM_NAME]))
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
            Key={QUESTIONS_ID_NAME: question_item["question-id"]}
        )
        print(f"db question: {question}")

        print(f"question item: {question_item}")
        qnas[question["Item"]["content"]] = question["Item"]["answer"]

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
            UpdateExpression="SET answer = :answer",
            ExpressionAttributeValues={":answer": question_item["answer"]},
        )

    previous_ending = get_prev_chapter_end(user_id)
    print(f"previous ending {previous_ending}")

    questionnaire = get_qnas(questions)
    print(f"questionnaire {questionnaire}")

    # Start a conversation with the user message.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    ai_intro_gen_query = f"""
        You are crafting an interactive narrative designed to explore emotional experiences through storytelling. This is part of a therapeutic exercise using CBT principles.
        Context: You previously wrote: {previous_ending}
        Emotional Check-in: {questionnaire}
        Your Task:
        Write a 350-400 word introspective scene featuring a gender-neutral character navigating a relatable, everyday situation. The scene should:

        Reflect the emotional themes from the questionnaire responses naturally within the narrative
        Use internal monologue to show the character's thought patterns, beliefs, and emotional reactions
        Ground the story in concrete, sensory details - what the character sees, hears, feels physically
        Build toward a meaningful decision point that connects to the character's emotional state
        Avoid dramatic extremes - keep situations realistic and relatable (workplace moments, social interactions, personal routines, family dynamics)
        Show, don't tell - reveal emotions through thoughts and physical sensations rather than labeling them

        Style Guidelines:

        Use present tense for immediacy
        Keep the character's name ambiguous or use "they/them"
        Focus on one specific moment or scene
        End at a natural decision point where the character must choose how to respond

        Format your response exactly as:
        [story text] || [choice 1] || [choice 2] || [choice 3]
        Each choice should be 6-10 words and represent meaningfully different approaches to the situation (e.g., avoidance vs. engagement, emotional vs. rational response, self-compassionate vs. self-critical). The choices should feel authentic to what someone might actually consider in that moment.
        Do not include labels, headers, or explanatory text - only the story and three choices separated by || 
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
            INTRO_CONTENT_NAME: content,
            INTRO_OPTIONS_NAME: options_list,
        }
    )

    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}}
