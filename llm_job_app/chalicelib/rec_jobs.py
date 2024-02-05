import pdftotext
from aws.opensearch import OpenSearch_custom
from llm_chain.chain.parser_resume import ResumeParserLLM, json_sample_schema_resume
from llm_chain.embedding import EmbeddingModel

os_client = OpenSearch_custom(
    host="search-ui-test-j4slt3fz7uu5ahsm6vgu3hwqem.us-east-2.es.amazonaws.com"
)
embedder = EmbeddingModel(model="text-embedding-ada-002")


def recommend_jobs(file_path):
    """
    Recommends jobs based on the provided resume file.

    Args:
        file_path (str): The path to the resume file.

    Returns:
        list: A list of recommended jobs.
    """

    with open(file_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Read all the text into one string
    pdftotext_text = "\n\n".join(pdf)

    resume_parser = ResumeParserLLM(model="gpt-3.5-turbo-1106")
    parsed_resume = resume_parser.parse(pdftotext_text, json_sample_schema_resume)

    serialized_string = ", ".join(f"{k}: {v}" for k, v in parsed_resume.items() if v)
    resume_embedding = embedder.get_embedding(text=serialized_string)

    # Search for jobs
    jobs = os_client.search_vector(
        index_name="jobs-index-vector",
        query=resume_embedding,
    )

    return jobs


if __name__ == "__main__":
    file_path = "data/Resume_Yusa_Li_MLE.pdf"
    jobs = recommend_jobs(file_path)
    print(jobs)
