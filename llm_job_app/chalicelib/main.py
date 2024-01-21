from apify.apify_actor_call import run_actor
from apify.scrapped_formatting import filter_full_job_info

# from aws.opensearch import save_to_index, create_index
from aws.opensearch_class import OpenSearch_custom

from llm_chain.custom_chain import JobParserLLM, json_parsed_sample

import os
from dotenv import load_dotenv
import logging
import time

import sys

# # Add a logging handler that directs logs to the terminal
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# # Set up logging
# logging.basicConfig(
#     filename="main.log",
#     level=logging.INFO,
#     filemode="w",
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

load_dotenv()


default_index_name = "llm-jobs-index"
index_name = "parsed-jobs-index-new"  # "parsed-jobs-index-w-date"

host = "search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"

os_client = OpenSearch_custom(host=host)
chat = JobParserLLM(model="gpt-3.5-turbo-1106")


def apify_get_clean(query_URL):
    jobs = run_actor(query_URL)
    batch_jobs = []
    start_time = time.time()  # Start time
    total_pages = len(jobs)  # Total number of pages

    for page_num, page in enumerate(jobs):
        jobs_info = page["googleJobs"]
        for job in jobs_info:
            # Clean the data
            # job = filter_full_job_info(job)

            try:
                # Parse the job description
                job_parsed = chat.parse(job, json_parsed_sample=json_parsed_sample)

                # Save the job to OpenSearch
                os_client.save_to_index(job_parsed, index_name=index_name)
            except Exception as e:
                print(f"==========Error: {e}==========")
                continue

            batch_jobs.append(job_parsed)

        logging.info(f"{page_num} / {total_pages} finished.")

    end_time = time.time()  # End time
    elapsed_time = end_time - start_time  # Time spent
    num_jobs = len(batch_jobs)  # Number of jobs scraped

    logging.info(f"Time spent: {elapsed_time:.0f} seconds")
    logging.info(f"Number of jobs scraped: {num_jobs}")

    return batch_jobs


def main():
    # Create the index if not exist
    os_client.create_index(index_name=index_name)

    query = "data science or data engineer or machine learning engineer jobs in Canada"
    q_string = query.replace(" ", "+")
    query_URL = f"https://www.google.com/search?q={q_string}&oq=google+jobs&ibp=htl;jobs&htivrt=jobs&htichips=date_posted:today&htischips=date_posted;today"

    jobs = apify_get_clean(query_URL)

    # print(jobs)
    return jobs


if __name__ == "__main__":
    main()
