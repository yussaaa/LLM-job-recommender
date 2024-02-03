from llm_chain.chain.parser import ParserLLM
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

json_sample_schema_job = {
    "job": {
        "title": "Machine Learning Engineer",
        "company": "Google",
        "industry": "Technology",
        "location": "Vancouver, BC",
        "years_of_experience_required": "3+ years",
        "employment_type": "Full-time",
        "source": "LinkedIn",
        "application_link": "https://...",
        "description": "Detailed job description goes here...",
    },
    "skills": {
        "programming_languages": ["Python", "Rust", "Go", "JavaScript"],
        "data_visualization_tools": ["Tableau", "PowerBI", "Looker"],
        "databases": ["PostgreSQL", "MySQL", "MongoDB"],
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
    "company_culture": [
        "work-life balance",
        "team environment",
        "flexible hours",
        "diversity",
    ],
    "job_benefits": {
        "salary_range": "100k - 150k",
        "salary_currency": "CAD",
        "paid_time_off": "14 days",
        "retirement_plan_matching": True,
        "professional_development_budget": "$1500",
        "employee_discounts": "20% off up to $5000 yearly",
        "remote_work_policy": {
            "fully_remote_option": False,
            "partial_remote_option": "2 days/week",
            "work_from_anywhere_program": "Up to 90 days/year",
        },
        "relocation_support": False,
    },
}


class JobParserLLM(ParserLLM):
    """
    This class represents a job parser for the LLM chain.

    It provides methods to parse job descriptions into a Python dictionary literal,
    extract pertinent details, and categorize them under the corresponding keys in the dictionary.

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
                template="As an AI assistant, your task is to parse job descriptions into a Python dictionary literal. \
              Upon receiving a job description, extract the pertinent details and categorize them under the corresponding keys in the dictionary, similar to the provided example. \
              If the job description does not explicitly mention a certain field, assign an empty string to that field. \
              Ensure that the output is a dictionary object, following the structure of the example provided. \
              {json_sample_schema} \ Note: The job description may not contain all the necessary information. Only populate the fields for which information is explicitly given or can be inferred with reasonable confidence.",
                input_variables=["json_sample_schema"],
            )
        )

    def get_human_message_prompt(self, json):
        """
        Returns a human message prompt template.

        Args:
            json (str): The JSON job description.

        Returns:
            HumanMessagePromptTemplate: The human message prompt template.
        """
        return HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="The following is the job description \n {json}?",
                input_variables=["json"],
            )
        )

    # def run_chain(self, chain, json_sample_schema, json_input):
    #     return chain.run(json_sample_schema=json_sample_schema, json=json_input)


if __name__ == "__main__":
    chat_job = JobParserLLM(model="gpt-3.5-turbo-1106")

    # with open("data/output.json", "r") as f:
    #     json_input = json.load(f)
    # # sample_jd = json_input[0]["googleJobs"][0]

    sample_jd = {
        "title": "Machine Learning Engineer - Canada",
        "companyName": "Inworld AI",
        "location": " Anywhere ",
        "via": "via Karkidi",
        "description": "At Inworld, we’re building the future of immersive experiences. Our mission is to create and inspire new meaningful relationships. We provide a creative suite for building virtual characters, with a focus on gaming and brand experiences. Our goal is to give creators an intuitive and powerful way to create lifelike, engaging, and expressive personalities.\n\nInworld AI is funded by top-tier investors, including Kleiner Perkins, Intel, Microsoft, and Founders Fund, and a team of all-star angels - corporate executives, top VC funds' partners, and industry veterans from Riot Games, Twitch, and Oculus.\n\nWe are seeking a Senior or higher-level Machine Learning Engineer with extensive experience working with generative large language models. You will be at the forefront of building generative AI products that utilize generative Large Language Models (LLMs) to create next-generation AI characters.\n\nQualifications\n• Bachelor’s degree or equivalent practical experience.\n• 5 years of experience... with software development in one or more programming languages, or 3 years of experience with an advanced degree.\n• 3 years of experience with applying machine learning algorithms in natural language processing domains.\n• 1+ years of experience training or fine-tuning generative LLMs (6B parameters and larger) such as GPT3, PaLM, etc.\n• Programming experience in Python.\n• Deep knowledge of machine learning frameworks such as PyTorch or JAX.\n• Experience with Triton is a big plus.\n\nResponsibilities\n• Explore artificial intelligence methods to support content creation, language understanding, etc.\n• Develop and test production-grade scalable generative machine learning models.\n• Create and verify the latest research methods for controllable text and code generation.\n• Develop and test data processing pipelines.\n\nNo suitable occupation? Feel free to send us your resume at career@inworld.ai",
        "jobHighlights": [
            {
                "items": [
                    "At Inworld, we’re building the future of immersive experiences. Our mission is to create and inspire new meaningful relationships. We provide a creative suite for building virtual characters, with a focus on gaming and brand experiences. Our goal is to give creators an intuitive and powerful way to create lifelike, engaging, and expressive personalities.\n\nInworld AI is funded by top-tier investors, including Kleiner Perkins, Intel, Microsoft, and Founders Fund, and a team of all-star angels - corporate executives, top VC funds' partners, and industry veterans from Riot Games, Twitch, and Oculus.\n\nWe are seeking a Senior or higher-level Machine Learning Engineer with extensive experience working with generative large language models. You will be at the forefront of building generative AI products that utilize generative Large Language Models (LLMs) to create next-generation AI characters.\n\nQualifications\n• Bachelor’s degree or equivalent practical experience.\n• 5 years of experience... with software development in one or more programming languages, or 3 years of experience with an advanced degree.\n• 3 years of experience with applying machine learning algorithms in natural language processing domains.\n• 1+ years of experience training or fine-tuning generative LLMs (6B parameters and larger) such as GPT3, PaLM, etc.\n• Programming experience in Python.\n• Deep knowledge of machine learning frameworks such as PyTorch or JAX.\n• Experience with Triton is a big plus.\n\nResponsibilities\n• Explore artificial intelligence methods to support content creation, language understanding, etc.\n• Develop and test production-grade scalable generative machine learning models.\n• Create and verify the latest research methods for controllable text and code generation.\n• Develop and test data processing pipelines.\n\nNo suitable occupation? Feel free to send us your resume at career@inworld.ai"
                ]
            }
        ],
        "relatedLinks": [
            {
                "link": "https://www.google.com/search?sca_esv=600158367&q=Inworld+AI&sa=X&ved=0ahUKEwjKkIngxO2DAxUmkWoFHb6TB4AQmJACCPgO",
                "text": "See web results for Inworld AI",
            }
        ],
        "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvRe3ktZu9tAbOmzhyRyPADKtU77MjRhcBQ333tM4&s",
        "extras": ["CA$220K–CA$350K a year", "Work from home", "Full-time"],
        "metadata": {"scheduleType": "Full-time", "workFromHome": True},
        "applyLink": {
            "title": "Apply on Karkidi",
            "link": "https://www.karkidi.com/job-details/39159-machine-learning-engineer-canada-job?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
        },
    }

    parsed_jd = chat_job.parse(
        json_input=sample_jd, json_sample_schema=json_sample_schema_job
    )
    print(type(parsed_jd), "\n", parsed_jd)
