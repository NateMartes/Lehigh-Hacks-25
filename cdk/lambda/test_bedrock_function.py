import boto3


def lambda_handler(event, context):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Amazon Nova Lite.
    model_id = "amazon.nova-lite-v1:0"

    # Start a conversation with the user message.
    user_message = input()
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

    return {"statusCode": 200, "body": response_text}
