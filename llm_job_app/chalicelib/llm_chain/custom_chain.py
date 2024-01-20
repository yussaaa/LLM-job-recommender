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


json_parsed_sample = {
    "job_basics": {
        "title": "Machine Learning Engineer",
        "company": "Google",
        "industry": "Technology",
        "location": "Vancouver, BC",
        "years_of_experience_required": "3+ years",
        "employment_type": "Full-time",
        "source": "LinkedIn",
        "application_link": "https://...",
    },
    "required_skills": {
        "programming_languages": ["Python", "Rust", "Go", "JavaScript"],
        "data_visualization_tools": ["Tableau", "PowerBI", "Looker"],
        "databases": ["PostgreSQL", "MySQL", "MongoDB"],
        "web_development": {
            "front_end_technologies": ["HTML", "CSS", "React", "Flask"],
            "back_end_technologies": ["Node.js", "Django"],
        },
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


class JobParserLLM:
    def __init__(
        self, model="gpt-4-1106-preview", temperature=0.9, max_tokens=3000, **kwargs
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
                template="As an AI assistant, your task is to parse job descriptions into a structured python dictionary object. \
              Upon receiving a job description, extract the pertinent details and categorize them under the corresponding keys in the dictionary, similar to the provided example. \
              If the job description does not explicitly mention a certain field, use your AI capabilities to infer the information. If inference is not possible, assign an empty string to that field. \
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

        try:
            parsed_jd = chain.run(json_parsed_sample=json_parsed_sample, json=json_jd)
            job_data_dict = ast.literal_eval(parsed_jd)
            return job_data_dict

        except Exception as e:
            print("Error occurred:", str(e))


if __name__ == "__main__":
    chat = JobParserLLM(model="gpt-3.5-turbo-1106")
    import json

    with open("data/output.json", "r") as f:
        json_jd = json.load(f)

    parsed_jd = chat.parse(
        json_jd=json_jd[0]["googleJobs"][0], json_parsed_sample=json_parsed_sample
    )
    print(type(parsed_jd), "\n", parsed_jd)
