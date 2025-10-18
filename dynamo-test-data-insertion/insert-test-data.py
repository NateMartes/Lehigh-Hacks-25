import boto3
import json
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")

# Mapping of JSON files to their respective DynamoDB tables
file_to_table = {
    "intro-sample.json": "intro",
    "end-sample.json": "End",
    "chapters-sample.json": "Chapters",
    "questions-sample.json": "questions",
}


def load_json_file(file_path):
    """Load and return data from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}.")
        return []


def batch_write_items(table_name, items):
    """Perform batch write to a DynamoDB table."""
    table = dynamodb.Table(table_name)
    try:
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        print(f"Successfully inserted {len(items)} items into table {table_name}.")
    except ClientError as e:
        print(
            f"Error inserting items into {table_name}: {e.response['Error']['Message']}"
        )


def main():
    """Main function to process each JSON file and insert data into DynamoDB."""
    for file_path, table_name in file_to_table.items():
        print(f"Processing {file_path} for table {table_name}...")
        items = load_json_file(file_path)
        if items:
            batch_write_items(table_name, items)
        else:
            print(f"No items to insert for {file_path}.")


if __name__ == "__main__":
    main()
