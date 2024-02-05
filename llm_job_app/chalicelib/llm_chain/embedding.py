from openai import OpenAI


class EmbeddingModel:
    def __init__(self, model: str = "text-embedding-ada-002"):
        """
        Initialize the EmbeddingModel class.

        Args:
            model (str, optional): The name of the model to use for embedding. Defaults to "text-embedding-ada-002".
        """
        self.model = model
        self.client = OpenAI()

    def get_embedding(self, text: str):
        """Embedding using OpenAI API

        Args:
            text (str): full text job description

        Returns:
            _type_: _description_
        """
        text = text.replace("\n", " ")

        return (
            self.client.embeddings.create(input=[text], model=self.model)
            .data[0]
            .embedding
        )


if __name__ == "__main__":
    embedder = EmbeddingModel(model="text-embedding-ada-002")
    job_parsed_filtered_str = "programming_languages: ['Python', 'Java'], devops_tools: ['Docker', 'Kubernetes', 'OpenShift'], machine_learning_operations: ['MLOps'], big_data_technologies: ['Apache Spark', 'Hadoop'], title: Principal Engineer - AI & Machine Learning, company: Royal Bank of Canada, industry: Wealth Management, location: Toronto, ON, Canada"

    embedding = embedder.get_embedding(job_parsed_filtered_str)
    print(len(embedding))
