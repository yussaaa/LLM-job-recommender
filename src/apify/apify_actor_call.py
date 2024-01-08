from apify_client import ApifyClient

import os
from dotenv import load_dotenv

load_dotenv()

# Access the variables
APIFY_TOKEN = os.getenv("APIFY_TOKEN")


# class ApifyHelper(ApifyClient):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._user_agent = "ApifyHelper/0.1.0"
#         self._user_agent += f" ({self._user_agent})"

# def _request(self, method, url, **kwargs):
#     kwargs['headers'] = kwargs.get('headers', {})
#     kwargs['headers']['User-Agent'] = self._user_agent
#     return super()._request(method, url, **kwargs)

# TODO: Add parameters on job filters, job titles, location, etc.


def run_actor():
    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_TOKEN)

    # Prepare the Actor input
    run_input = {
        "queries": "Teacher\nhttps://www.google.com/search?q=doctor&ibp=htl;jobs",
        "maxPagesPerQuery": 1,
        "csvFriendlyOutput": False,
        "languageCode": "",
        "maxConcurrency": 10,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": False,
        "includeUnfilteredResults": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("SpK8RxKhIgV6BWOz9").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    # for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    #     print(item)

    return client.dataset(run["defaultDatasetId"]).list_items().items
