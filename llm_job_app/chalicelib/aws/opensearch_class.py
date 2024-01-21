import boto3
import requests
import os
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth


class OpenSearch_custom:
    def __init__(
        self, host, service="es", credentials=boto3.Session().get_credentials()
    ):
        self.hosts = host
        self.awsauth = AWS4Auth(
            os.getenv("AWS_ACCESS_KEY_ID"),
            os.getenv("AWS_SECRET_ACCESS_KEY"),
            "us-east-2",
            service,
            session_token=credentials.token,
        )
        self.client = self._creat_client(self.hosts)

    def _creat_client(self, host):
        return OpenSearch(
            hosts=[{"host": host, "port": 443}],
            http_auth=self.awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

    def save_to_index(self, dict_data: dict, index_name: str):
        """Save the data to OpenSearch index

        Args:
            dict_data (dict): data to be saved
            index_name (str): index name
        """
        try:
            # Save the dictionary to OpenSearch
            response = self.client.index(
                index=index_name, body=dict_data, pipeline="add-timestamp"
            )
            # Print the response
            print(response)
        except Exception as e:
            print(e)
            print("=========Error saving to index for the following data:=========\n")
            print(dict_data)
            print()

    def create_index(self, index_name: str):
        # Create an index with non-default settings.
        # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html#bp-sharding
        # shards should correspond to 10-30GB where search latency is objective
        # should be 30-50GB for write-heavy jobs like log analytics
        # by default, each index == 5 primary shards + 1 replica/primary == 10x total shards
        # replica shard == copy of a primary shard
        # shards are distributed amongst nodes for resilience
        # index > shards > multiple nodes (assuming you have more than 1)
        # lower shard count == faster reads
        # higher shard count == faster writes
        index_body = {"settings": {"index": {"number_of_shards": 1}}}

        try:
            if self.client.indices.exists(index=index_name):
                print(f"Index {index_name} already exists")
                return
            response = self.client.indices.create(
                index_name,
                body=index_body,
                # pipeline="add-timestamp",
            )
            print("\nCreating index:")
            print(response)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    host = "search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"
    os_client = OpenSearch_custom(host=host)
    index_name = "parsed-jobs-index"
    # os_client.create_index(index_name=index_name)
    # job_parsed = {\n  "job_basics": {\n    "title": "Sr Data Engineer",\n    "company": "Royal Bank of Canada",\n    "industry": "Banking/Financial Services",\n    "location": "Toronto, ON, Canada",\n    "years_of_experience_required": "5+ years",\n    "employment_type": "Full-time",\n    "source": "Jobs At RBC",\n    "application_link": "https://jobs.rbc.com/ca/en/job/R-0000076286/Sr-Data-Engineer?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic"\n  },\n  "required_skills": {\n    "programming_languages": ["Python", "SQL"],\n    "data_visualization_tools": [],\n    "databases": ["NoSQL", "SQL databases"],\n    "web_development": {\n      "front_end_technologies": [],\n      "back_end_technologies": []\n    },\n    "devops_tools": [],\n    "statistical_analysis_methods": [],\n    "machine_learning_frameworks": [],\n    "machine_learning_operations": [],\n    "cloud_platforms": ["Azure", "Snowflake"],\n    "big_data_technologies": ["Hadoop", "PySpark"],\n    "natural_language_processing": [],\n    "deep_learning_concepts": [],\n    "data_engineering_tools": ["ETL/ELT workflows"],\n    "large_models": []\n  },\n  "company_culture": [\n    "diversity and inclusion",\n    "equitable workplace",\n    "coaching and mentoring"\n  ],\n  "job_benefits": {\n    "salary_range": "",\n    "salary_currency": "CAD",\n    "paid_time_off": "",\n    "retirement_plan_matching": false,\n    "professional_development_budget": "",\n    "employee_discounts": "",\n    "remote_work_policy": {\n      "fully_remote_option": false,\n      "partial_remote_option": "",\n      "work_from_anywhere_program": ""\n    },\n    "relocation_support": ""\n  }\n}\n```'
    job_parsed = {
        "job": {
            "title": "Principal Engineer - AI & Machine Learning",
            "company": "Royal Bank of Canada",
            "industry": "Wealth Management",
            "location": "Toronto, ON, Canada",
            "years_of_experience_required": "",
            "employment_type": "Full time",
            "source": "RBC Careers",
            "application_link": "https://jobs.rbc.com/ca/en/job/R-0000075808/Principal-Engineer-AI-Machine-Learning?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
        },
        "skills": {
            "programming_languages": ["Python", "Java"],
            "data_visualization_tools": [],
            "databases": [],
            "web_development": {
                "front_end_technologies": [],
                "back_end_technologies": [],
            },
            "devops_tools": ["Docker", "Kubernetes", "OpenShift"],
            "statistical_analysis_methods": [],
            "machine_learning_frameworks": [],
            "machine_learning_operations": ["MLOps"],
            "cloud_platforms": [],
            "big_data_technologies": ["Apache Spark", "Hadoop"],
            "natural_language_processing": [],
            "deep_learning_concepts": [],
            "data_engineering_tools": [],
            "large_models": [],
        },
        "company_culture": [
            "Flexible work/life balance options",
            "Leaders who support your development through coaching and managing opportunities",
        ],
        "job_benefits": {
            "salary_range": "",
            "salary_currency": "",
            "paid_time_off": "",
            "retirement_plan_matching": False,
            "professional_development_budget": "",
            "employee_discounts": "",
            "remote_work_policy": {
                "fully_remote_option": False,
                "partial_remote_option": "",
                "work_from_anywhere_program": "Up to 90 days/year",
            },
            "relocation_support": False,
        },
    }

    os_client.save_to_index(job_parsed, index_name=index_name)
