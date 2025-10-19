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

MODEL_ID = "us.meta.llama3-3-70b-instruct-v1:0"


def gen_prompt(prev_end):
    if not prev_end:
        return """
            You are a CBT (Cognitive Behavioral Therapy) therapist conducting an initial assessment. Your goal is to identify key cognitive distortions, behavioral patterns, and emotional triggers that will inform a personalized therapeutic story.

            Generate exactly 5 yes/no screening questions that:
            - Assess different aspects of the patient's mental state (thoughts, feelings, behaviors, relationships, self-perception)
            - Identify specific cognitive distortions (all-or-nothing thinking, catastrophizing, overgeneralization, etc.)
            - Uncover avoidance behaviors or unhelpful coping mechanisms
            - Are clear, direct, and non-judgmental
            - Progress from general to more specific concerns

            Format: Output ONLY the 5 questions separated by the | symbol. No introductions, explanations, or additional text.

            Example format:
            Do you often feel that small mistakes mean you've completely failed? | Do you find yourself avoiding social situations because you worry about being judged? | [etc.]
        """

    return f"""
        You are a CBT therapist conducting a follow-up assessment after a previous therapeutic story intervention.

        CONTEXT FROM LAST SESSION:
        - Patient's chosen action: {prev_end[END_CHOICE_NAME]}
        - Story outcome: {prev_end[END_CONTENT_NAME]}

        Generate exactly 5 yes/no screening questions that:
        - Assess whether the patient implemented insights from the previous story in real life
        - Identify any shifts in thinking patterns or behavioral responses since last session
        - Explore obstacles or resistance encountered when trying new approaches
        - Evaluate emotional responses to the previous story's themes
        - Determine if previous cognitive distortions persist or have evolved
        - Progress logically from reflection on past actions to current state

        Questions should:
        - Reference the previous story's themes or choices naturally (without being overly specific)
        - Feel conversational and supportive, not like a test
        - Help determine what therapeutic direction the next story should take
        - Assess both successes and struggles without judgment

        Format: Output ONLY the 5 questions separated by the | symbol. No introductions, explanations, numbering, or additional text.

        Example format:
        Since our last conversation, have you noticed yourself catching negative thoughts before they spiral? | Did you try any of the approaches we explored in the story? | [etc.]
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

    prompt = gen_prompt(prev_end)

    conversation = [{"role": "user", "content": [{"text": prompt}]}]

    ai_response = client.converse(
        modelId=MODEL_ID,
        messages=conversation,
        inferenceConfig={"temperature": 0.5, "topP": 0.9},
    )
    ai_response_text = ai_response["output"]["message"]["content"][0]["text"]

    questions = ai_response_text.split("|")
    questions = filter(lambda x: x != "" and not x.isspace(), questions)
    questions = [q.strip() for q in questions]

    for i in range(len(questions)):
        questions_table.put_item(
            Item={
                CHAPTERS_KEY_NAME: ch_key,
                QUESTIONS_ID_NAME: str(uuid.uuid4()),
                QUESTIONS_CONTENT_NAME: questions[i],
                QUESTIONS_ANSWER_NAME: None,
            }
        )

    return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"}}
