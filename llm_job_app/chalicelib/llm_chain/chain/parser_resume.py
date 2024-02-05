from llm_chain.chain.parser import ParserLLM
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

json_sample_schema_resume = {
    "job": {
        "titles_worked": [
            "Machine Learning Engineer",
            "Data Scientist",
            "Data Analyst",
        ],
        "company_worked": ["Google", "Microsoft", "Apple"],
        "industry": ["Technology"],
        "location": "Vancouver, BC",
        "years_of_experience": "10+ years",
        "summary": "Personal summary goes here...",
    },
    "skills": {
        "programming_languages": ["Python", "Rust", "Go", "JavaScript"],
        "data_visualization_tools": ["Tableau", "PowerBI", "Looker"],
        "database": ["PostgreSQL", "MySQL", "MongoDB"],
        "web_dev_front_end": ["HTML", "CSS", "React"],
        "web_dev_back_end": ["Node.js", "Django", "Flask"],
        "devops_tools": ["Git", "Docker", "Kubernetes"],
        "statistical_analysis_methods": ["Linear Regression", "Logistic Regression"],
        "machine_learning_frameworks": [
            "PyTorch",
            "TensorFlow",
            "Scikit-learn",
            "hugingface",
        ],
        "machine_learning_operations": [
            "MLFlow",
            "Kubeflow",
            "Seldon",
        ],
        "cloud_platforms": ["AWS", "GCP", "Azure"],
        "big_data_technologies": ["Hadoop", "Spark"],
        "natural_language_processing": ["NLTK", "SpaCy"],
        "deep_learning_concepts": ["CNN", "RNN", "LSTM"],
        "data_engineering_tools": ["Airflow", "Luigi"],
        "large_models": ["GPT-3", "BERT", "Transformer-based models"],
    },
}


class ResumeParserLLM(ParserLLM):
    """
    A class that represents a resume parser for LLM.

    This class provides methods to parse resumes into a Python dictionary literal.
    It extracts pertinent details such as personal information, skills, education, and work experience,
    and categorizes them under the corresponding keys in the dictionary.

    Attributes:
        None

    Methods:
        get_system_message_prompt(json_sample_schema): Returns a system message prompt template.
        get_human_message_prompt(json): Returns a human message prompt template.
    """

    def get_system_message_prompt(self, json_sample_schema):
        """
        Returns a system message prompt template.

        Args:
            json_sample_schema (str): The JSON sample schema.

        Returns:
            SystemMessagePromptTemplate: The system message prompt template.
        """
        return SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="As an AI assistant, your task is to parse resumes into a Python dictionary literal. \
                  Upon receiving a resume, extract the pertinent details such as personal information, skills, education, and work experience, and categorize them under the corresponding keys in the dictionary, similar to the provided example. \
                  If the resume does not explicitly mention a certain field, assign an empty string to that field. \
                  Ensure that the output is a dictionary object, following the structure of the example provided. \
                 {json_sample_schema} \ Note: The resume may not contain all the necessary information. Only populate the fields for which information is explicitly given or can be inferred with reasonable confidence.",
                input_variables=["json_sample_schema"],
            )
        )

    def get_human_message_prompt(self, json):
        """
        Returns a human message prompt template.

        Args:
            json (str): The JSON resume.

        Returns:
            HumanMessagePromptTemplate: The human message prompt template.
        """
        return HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="The following is the resume \n {json}",
                input_variables=["json"],
            )
        )


if __name__ == "__main__":
    chat_resume = ResumeParserLLM(model="gpt-3.5-turbo-1106")

    # with open("data/output.json", "r") as f:
    #     json_input = json.load(f)
    # # sample_jd = json_input[0]["googleJobs"][0]

    sample_resume = "Yusa Li\nToronto, ON, M4Y 0E8 | 780-707-7844 | yusa.li@hotmail.com | linkedin.com/in/yusa-li/ | github.com/yussaaa\nCurious sponge that always absorbs trending technologies and aims to tackle impactful problems\n\nSKILLS\nCloud & Infrastructure: Azure · AWS · GCP · Spark · Kubeflow · Databricks · Terraform · Docker · Kubernetes\nMachine Learning:\nPyTorch · TensorFlow · scikit-learn · Pandas · NumPy · Spacy · Label Studio · Great Expectations · MLflow\nProgramming:\nPython · Rust · Golang · SQL · NoSQL · Shell · Git · Flask · LangChain · Airflow · Kafka · RabbitMQ\nAnalytics & Visualization: Tableau · Power BI · SparkSQL · BigQuery · Azure Synapse · Matplotlib · Seaborn · Plotly\nCertification:\nAzure Data Scientist Associate · AWS Solution Architect Associate · GCP Professional MLE (Exam scheduled)\n\nPROFESSIONAL EXPERIENCE\nStatistic Canada – Consumer Price Division\nToronto\nMachine Learning Engineer\nFeb 2022 – June 2023\n• Developed and deployed MLOps data validation pipeline on AzureML. Built data validation rules using Great Expectations\n• Contributed to Great Expectations open-source community with custom expectation for null value check\n• Orchestrated pipeline components such as classifier, data validation, outlier detection resulting 90% reduction of work effort\n• Provisioned infrastructure such as cluster size, compute size and Azure ML workspace using Terraform\n• Built and deploy CI/CD pipeline on GitLab with unit testing with pytest and linting checks\n• Fine-tuned BERT based model with PyTorch on NLP classification and NER task. Tracked experiments using Weight and Bias\nData Scientist\nDec 2020 – Feb 2022\n• Developed a Named Entity Recognition model for extracting electronic product features. Full ML cycle was practiced from\ndata labelling (hosting Label Studio docker image on Azure App Service), concept validation to model building (Spacy)\n• Scraped text description data using Beautiful Soup and selenium. Prototyped NER service with Azure cognitive service\n• Trained and deployed NLP classification model on Azure ML, experimented and tracked with MLflow\n• Built Amazon product historical price tracking tool using Keepa and Python. Visualized in PowerBI dashboard\nBMO-Global Asset Management\nToronto\nDatabase Analyst\nMar 2020 – May 2020\n• Automated portfolio reporting process by extracting and transforming millions of rows of equity data using Azure Synapse\n• Designed and executed testing plan to evaluate and ensure data quality using SQL, Excel functions, pivot tables, Power BI\n• Communicated with stakeholders to gather accurate requirements for the Business Intelligence report\n\nPROJECTS\nJob recommender system with LLM, RAG and LangChain (Ongoing)\n• Built a job recommender app to 1. Extract and summarize PDF resumes 2. Parse LinkedIn job postings 3. Periodically parse\nlatest job postings Apify 4. Send user daily recommended job email with unmatched skill summary\n• Implemented job parsing with Beautiful Soup and Selenium; Front-end build with Streamlit; Emails sent with AWS SNS\n• Automated a serverless ETL pipeline using AWS Lambda and EventBridge, storing cleaned job descriptions as JSON in\nOpenSearch and saving transformed embeddings to Pinecone VectorDB\n• Engineered the OpenAI prompts to conduct summarization and comparison tasks; Connected Chains using LangChain\n• Recommend top matched 20 jobs based on semantic search result between embeddings of user’s resume and JDs\nFull Stack Transfer learning food classifier with PyTorch and TensorFlow\n• Loaded pre-trained feature and fine-tuned the model using the Food101 dataset\n• Compared between 30Mb EffnetB2 and 295Mb ViT-b-16 model. Opted EffnetB2 for production due to its size advantage\n• Built Gradio app with the trained model and deployed the app to Hugging Face Space\n\nEDUCATION\nMaster of Engineering, Industrial Engineering (Emphasis on Analytics / Data Science)\nUniversity of Toronto\n\n2018 - 2019\n\nBachelor of Science, Mechanical Engineering\nUniversity of Alberta\n\n2014 - 2018\n\n\x0c"

    parsed_resume = chat_resume.parse(
        json_input=sample_resume, json_sample_schema=json_sample_schema_resume
    )
    print(type(parsed_resume), "\n", parsed_resume)
