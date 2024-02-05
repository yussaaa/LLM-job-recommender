## Explorer other saving options
import boto3


def prepare_data_to_dynamo_format(data: dict):
    """Prepare the data to be saved in DynamoDB

    Args:
        data (dict): data to be saved

    Returns:
        dict: data in DynamoDB format
    """

    return {
        "id": {"S": "1"},
        "job_title": {"S": data["title"]},
        "company_name": {"S": data["companyName"]},
        "location": {"S": data["location"]},
        "source": {"S": data["via"]},
        "full_text_description": {"S": data["description"]},
        "job_type": {"S": data["metadata"]},
        "link": {"S": data["applyLink"]},
    }


def save_to_dynamo(data: dict, table_name: str):
    """Save the data to DynamoDB

    Args:
        data (dict): data to be saved
    """

    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")

    # Save the dictionary to DynamoDB
    response = dynamodb.put_item(TableName=table_name, Item=data)

    # Print the response
    print(response)
