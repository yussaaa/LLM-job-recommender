from chalicelib.apify.apify_actor_call import run_actor
from chalicelib.apify.scrapped_formatting import filter_full_job_info

# from aws.opensearch import save_to_index, create_index
from chalicelib.aws.opensearch_class import OpenSearch_custom

import os
from dotenv import load_dotenv

load_dotenv()


default_index_name = "llm-jobs-index"
host = "search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"

os_client = OpenSearch_custom(host=host)


def apify_get_clean():
    jobs = run_actor()
    batch_jobs = []
    for page in jobs:
        jobs_info = page["googleJobs"]
        for job in jobs_info:
            # Clean the data
            job = filter_full_job_info(job)

            # Save the job to OpenSearch
            os_client.save_to_index(job, index_name=default_index_name)

            batch_jobs.append(job)

    print(len(batch_jobs), "been scraped and formatted.")
    return batch_jobs


def main():
    # Create the index if not exist
    os_client.create_index(index_name=default_index_name)

    jobs = apify_get_clean()

    print(jobs)
    return jobs


if __name__ == "__main__":
    main()