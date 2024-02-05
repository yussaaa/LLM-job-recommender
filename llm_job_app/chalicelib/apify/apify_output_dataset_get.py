import requests


def get_dataset_by_id(id: str, APIFY_TOKEN: str):
    """Get dataset by id

    Args:
        id (str): dataset id
        APIFY_TOKEN (str): apify token

    Returns:
        dict: REST JSON response
    """
    # Make the GET request
    response = requests.get(
        f"https://api.apify.com/v2/datasets/{id}/items?token={APIFY_TOKEN}"
    )
    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content as JSON
        data = response.json()
        return data
    else:
        print("Error: Failed to retrieve data")
        return None
