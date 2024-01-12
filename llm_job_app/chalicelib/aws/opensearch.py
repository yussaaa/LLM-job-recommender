import boto3
import requests
import os
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

region = "us-east-2"
service = "es"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    os.getenv("AWS_ACCOUNT_ID"),
    os.getenv("AWS_ACCESS_KEY"),
    region,
    service,
    session_token=credentials.token,
)

# The OpenSearch domain endpoint

host = "search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"

client = OpenSearch(
    hosts=[{"host": host, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


def save_to_index(dict_data: dict, index_name: str):
    """Save the data to OpenSearch index

    Args:
        dict_data (dict): data to be saved
        index_name (str): index name
    """
    # Save the dictionary to OpenSearch
    response = client.index(index=index_name, body=dict_data)

    # Print the response
    print(response)


def create_index(index_name: str):
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
        if client.indices.exists(index=index_name):
            print(f"Index {index_name} already exists")
            return
        response = client.indices.create(index_name, body=index_body)
        print("\nCreating index:")
        print(response)
    except Exception as e:
        print(e)
