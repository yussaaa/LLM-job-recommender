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


def run_actor(query_URL):
    # Initialize the ApifyClient with your API token
    client = ApifyClient(APIFY_TOKEN)

    # Prepare the Actor input
    run_input = {
        "queries": query_URL,
        "maxPagesPerQuery": 100,
        "csvFriendlyOutput": False,
        "languageCode": "",
        "maxConcurrency": 10,
        "saveHtml": False,
        "saveHtmlToKeyValueStore": False,
        "includeUnfilteredResults": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("SpK8RxKhIgV6BWOz9").call(run_input=run_input)

    parsed_jobs = client.dataset(run["defaultDatasetId"]).list_items().items

    return parsed_jobs


if __name__ == "__main__":
    query = "data science or data engineer or machine learning engineer jobs in Canada"
    q_string = query.replace(" ", "+")
    query_URL = f"https://www.google.com/search?q={q_string}&oq=google+jobs&ibp=htl;jobs&htivrt=jobs&htichips=date_posted:today&htischips=date_posted;today"

    parsed_jobs = run_actor(query_URL)

    num_pages_parsed = len(parsed_jobs)
    jobs_per_page = parsed_jobs[0]["searchQuery"]["resultsPerPage"]
    print(
        f"\nActor finished, approximately {num_pages_parsed} pages x {jobs_per_page} jobs/page = {num_pages_parsed * jobs_per_page} jobs are parsed."
    )
