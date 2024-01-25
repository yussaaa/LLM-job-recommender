from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

import ast
import json


# TODO: Infer the company industry from the company name


json_parsed_sample = {
    "job": {
        "title": "Machine Learning Engineer",
        "company": "Google",
        "industry": "Technology",
        "location": "Vancouver, BC",
        "years_of_experience_required": "3+ years",
        "employment_type": "Full-time",
        "source": "LinkedIn",
        "application_link": "https://...",
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

# "description": "Detailed job description goes here...",
# "full_text_of_benefits": "Full description of all benefits offered...",
# "posted_date": "2023-12-21",
# "posted_relative_date (days ago)": "2",


class JobParserLLM:
    def __init__(
        self, model="gpt-3.5-turbo-1106", temperature=0.1, max_tokens=3000, **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.chat = self.__init_llm()

    def __init_llm(self):
        return ChatOpenAI(
            model=self.model, temperature=self.temperature, max_tokens=self.max_tokens
        )

    def parse(self, json_jd, json_parsed_sample):
        system_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template="As an AI assistant, your task is to parse job descriptions into a Python dictionary literal. \
              Upon receiving a job description, extract the pertinent details and categorize them under the corresponding keys in the dictionary, similar to the provided example. \
              If the job description does not explicitly mention a certain field, assign an empty string to that field. \
              Ensure that the output is a dictionary object, following the structure of the example provided. \
              {json_parsed_sample} \ Note: The job description may not contain all the necessary information. Only populate the fields for which information is explicitly given or can be inferred with reasonable confidence.",
                input_variables=["json_parsed_sample"],
            )
        )

        # system_message_prompt_part1 = SystemMessagePromptTemplate(
        #     prompt=PromptTemplate(
        #         template="As an AI assistant, your task is to parse job descriptions into a structured python dictionary object. \
        #           Upon receiving a job description, extract the pertinent details and categorize them under the corresponding keys in the dictionary, similar to the provided example. \
        #           If the job description does not explicitly mention a certain field, use your AI capabilities to infer the information. If inference is not possible, assign an empty string to that field. \
        #           Ensure that the output is a dictionary object, following the structure of the example provided. \
        #           Note: The job description may not contain all the necessary information. Only populate the fields for which information is explicitly given or can be inferred with reasonable confidence.",
        #         input_variables=[],
        #     )
        # )

        # system_message_prompt_part2 = SystemMessagePromptTemplate(
        #     prompt=PromptTemplate(
        #         template="{json_parsed_sample}",
        #         input_variables=["json_parsed_sample"],
        #     )
        # )

        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="The following is the job description \n {json}?",
                input_variables=["json"],
            )
        )
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
            # [
            #     system_message_prompt_part1,
            #     system_message_prompt_part2,
            #     human_message_prompt,
            # ]
        )
        chain = LLMChain(llm=self.chat, prompt=chat_prompt_template)

        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                parsed_jd = chain.run(
                    json_parsed_sample=json_parsed_sample, json=json_jd
                )
                job_data_dict = ast.literal_eval(parsed_jd)
                return job_data_dict
            except Exception as e:
                attempts += 1
                print("----------------------------------------")
                print(f"Attempt {attempts} failed with error: {e}")
                if attempts < max_attempts:
                    print("Retrying...")
                else:
                    print("Max attempts reached. Handling error.")
                    print(f"When processing this job: \n{json_jd}")
                    print("----------------------------------------")


if __name__ == "__main__":
    chat = JobParserLLM(model="gpt-3.5-turbo-1106")

    # with open("data/output.json", "r") as f:
    #     json_jd = json.load(f)
    # # sample_jd = json_jd[0]["googleJobs"][0]

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

    parsed_jd = chat.parse(json_jd=sample_jd, json_parsed_sample=json_parsed_sample)
    print(type(parsed_jd), "\n", parsed_jd)
