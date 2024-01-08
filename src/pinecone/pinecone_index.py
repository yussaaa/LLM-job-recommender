import pinecone
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

PINECONE_INDEX = "jd-index"

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

pinecone.create_index(PINECONE_INDEX, dimension=1536, metric="cosine")
pinecone.describe_index(PINECONE_INDEX)

# TODO: Add error handling here if index not found


index = pinecone.Index(PINECONE_INDEX)


def embedding_index(embedding: list, index: pinecone.Index):
    index.upsert(
        vectors=[
            {"id": "job_0", "values": embedding},
        ],
        namespace="ns1",
    )


def embedding_search(embedding: list, index: pinecone.Index):
    results = index.query(
        vectors=[embedding],
        top_k=10,
        # query_params=pinecone.QueryParams(filter="ns1", max_distance=0.5),
    )
    return results


def show_index_status(index: pinecone.Index):
    print(index.describe())
    print(index.list_indexes())
    print(index.describe_index_stats())
