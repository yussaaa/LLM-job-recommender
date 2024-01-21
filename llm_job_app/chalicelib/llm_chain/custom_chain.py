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
        "web_development": {
            "front_end_technologies": ["HTML", "CSS", "React"],
            "back_end_technologies": ["Node.js", "Django", "Flask"],
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
                template="As an AI assistant, your task is to parse job descriptions into a structured dictionary. \
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
        "title": "Principal Engineer - AI & Machine Learning",
        "companyName": "Royal Bank of Canada",
        "location": "  Toronto, ON, Canada   ",
        "via": "via RBC Careers",
        "description": "Job Summary\n\nJob Description\n\nWhat is the opportunity?\n\nThe Principal Engineer, Machine Learning is a hands-on leadership role responsible for driving and executing the implementation of MLOps and machine learning solutions. This role involves a combination of technical expertise, hands-on execution, and strategic thinking to drive the application of machine learning techniques to solve highly complex business problems. The Principal Engineer works closely with cross-functional teams (business partners, data scientists, product managers), and provides technical guidance and mentorship, ensuring the implementation of best practices and the delivery of high-quality machine learning solutions.\n\nWhat Will you do?\n• Lead the development and integration of MLOps platform and technologies to automate and expedite delivery of AI/ML solutions at scale.\n• Create and maintain the technical roadmap for MLOps capabilities and own the delivery backlog. Partner closely with leaders from across GAM... and RBC to articulate GAM’s MLOps requirements, identify and incorporate Enterprise capabilities and support, and prioritize development of new capabilities.\n• Responsible for designing and implementing scalable, robust, and efficient ML systems and ensuring that ML infrastructure and pipelines are properly designed, optimized, and maintained.\n• Apply expertise in big data technologies such as Apache Spark, Hadoop, and related frameworks for scalable data processing and design and implement data pipelines for handling large volumes of data in AI/ML workflows.\n• Hands-on development and implementation support for MLOps capabilities within GAM. Establish cross-team partnerships with data engineers, software developers, and related teams from across RBC to develop, adopt, and influence emerging reusable enterprise technologies.\n• Collaborate with stakeholders from various teams, including data scientists, software engineers, and business leaders to effectively design and implement ML solutions that solve complex business problems.\n• Provide technical leadership and guidance based on a deep understanding of machine learning algorithms, frameworks, and tools, and expertise to make informed decisions regarding the selection and implementation of ML technologies and methodologies.\n• Establish and enforce best coding standards and practices for AI/ML development within the organization.\n• Play a vital role in mentoring and developing junior ML engineers and data scientists. Provide guidance, share best practices, and help team members grow their technical skills and knowledge. Follow, evaluate, and communicate the latest ML research, frameworks, and technologies to enhance the organization's ML capabilities.\n\nWhat do you need to succeed?\n\nMust Have\n• Extensive experience in AI/ML development and deployment, demonstrating a deep understanding of machine learning algorithms, models, and framework.\n• Proven expertise in MLOps, including the development and integration of MLOps platforms and technologies to automate the delivery of AI/ML at scale.\n• Strong proficiency in programming languages such as Python or Java, and experience with machine learning frameworks and libraries.\n• Experience with containerization technologies such as Docker, Kubernetes, and OpenShift for efficient deployment and management of AI/ML applications\n• Strong technology skills and expertise, with a focus on current and emerging big-data technologies relevant to model development and deployment (Python, PySpark, SQL, Docker, Dagster, Spark, S3, Trino, Tableau, classification models, propensity models, timeseries models, NLP, LLMs, neural networks, etc.).\n• Deep understanding of business context, objectives, and requirements. Ability to align ML solutions with business goals, identify opportunities for ML applications, and communicate the value and potential impact to the organization.\n• Excellent problem-solving skills and the ability to think critically and creatively.\n• Strong communication and presentation skills, with the ability to explain complex concepts to both technical and non-technical stakeholders.\n\nNice to Have\n• Bachelor's or Master's degree in Computer Science, Engineering, or a related field.\n• Demonstrated success in applying agile best-practices to frame problems and prioritize key outcomes; hypothesize, iterate, and continuously improve on solutions; and continuously deliver incremental value to end-users and key stakeholders.\n• Previous experience in the wealth and asset management industry.\n\nWhat’s in it for you?\n\nWe thrive on the challenge to be our best, progressive thinking to keep growing, and working together to deliver trusted advice to help our clients thrive and communities prosper. We care about each other, reaching our potential, making a difference to our communities, and achieving success that is mutual.\n• Opportunity to build cross platform experience – in a high growth strategic segment.\n• Opportunity to work with a strategic client segment and experience in unique / customized lending.\n• Opportunity to work with senior leaders across RBC including Wealth Management, Canadian Banking and Capital Markets.\n• A comprehensive Total Rewards Program including bonuses and flexible benefits, competitive compensation, commissions, and stock where applicable.\n• Leaders who support your development through coaching and managing opportunities.\n• Flexible work/life balance options.\n• Access to a variety of job opportunities across business and geographies.\n\nJob Skills\nBig Data Management, Cloud Computing, Database Development, Data Mining, Data Warehousing (DW), ETL Processing, Problem Solving, Quality Management, Requirements Analysis\n\nAdditional Job Details\n\nAddress:\n\nRBC CENTRE, 155 WELLINGTON ST W:TORONTO\n\nCity:\n\nTORONTO\n\nCountry:\n\nCanada\n\nWork hours/week:\n\n37.5\n\nEmployment Type:\n\nFull time\n\nPlatform:\n\nWealth Management\n\nJob Type:\n\nRegular\n\nPay Type:\n\nSalaried\n\nPosted Date:\n\n2024-01-10\n\nApplication Deadline:\n\n2024-01-28\n\nInclusion and Equal Opportunity Employment\n\nAt RBC, we embrace diversity and inclusion for innovation and growth. We are committed to building inclusive teams and an equitable workplace for our employees to bring their true selves to work. We are taking actions to tackle issues of inequity and systemic bias to support our diverse talent, clients and communities.\n\u200b\u200b\u200b\u200b\u200b\u200b\u200b\nWe also strive to provide an accessible candidate experience for our prospective employees with different abilities. Please let us know if you need any accommodations during the recruitment process.\n\nJoin our Talent Community\n\nStay in-the-know about great career opportunities at RBC. Sign up and get customized info on our latest jobs, career tips and Recruitment events that matter to you.\n\nExpand your limits and create a new future together at RBC. Find out how we use our passion and drive to enhance the well-being of our clients and communities at jobs.rbc.com",
        "jobHighlights": [
            {
                "items": [
                    "Job Summary\n\nJob Description\n\nWhat is the opportunity?\n\nThe Principal Engineer, Machine Learning is a hands-on leadership role responsible for driving and executing the implementation of MLOps and machine learning solutions. This role involves a combination of technical expertise, hands-on execution, and strategic thinking to drive the application of machine learning techniques to solve highly complex business problems. The Principal Engineer works closely with cross-functional teams (business partners, data scientists, product managers), and provides technical guidance and mentorship, ensuring the implementation of best practices and the delivery of high-quality machine learning solutions.\n\nWhat Will you do?\n• Lead the development and integration of MLOps platform and technologies to automate and expedite delivery of AI/ML solutions at scale.\n• Create and maintain the technical roadmap for MLOps capabilities and own the delivery backlog. Partner closely with leaders from across GAM... and RBC to articulate GAM’s MLOps requirements, identify and incorporate Enterprise capabilities and support, and prioritize development of new capabilities.\n• Responsible for designing and implementing scalable, robust, and efficient ML systems and ensuring that ML infrastructure and pipelines are properly designed, optimized, and maintained.\n• Apply expertise in big data technologies such as Apache Spark, Hadoop, and related frameworks for scalable data processing and design and implement data pipelines for handling large volumes of data in AI/ML workflows.\n• Hands-on development and implementation support for MLOps capabilities within GAM. Establish cross-team partnerships with data engineers, software developers, and related teams from across RBC to develop, adopt, and influence emerging reusable enterprise technologies.\n• Collaborate with stakeholders from various teams, including data scientists, software engineers, and business leaders to effectively design and implement ML solutions that solve complex business problems.\n• Provide technical leadership and guidance based on a deep understanding of machine learning algorithms, frameworks, and tools, and expertise to make informed decisions regarding the selection and implementation of ML technologies and methodologies.\n• Establish and enforce best coding standards and practices for AI/ML development within the organization.\n• Play a vital role in mentoring and developing junior ML engineers and data scientists. Provide guidance, share best practices, and help team members grow their technical skills and knowledge. Follow, evaluate, and communicate the latest ML research, frameworks, and technologies to enhance the organization's ML capabilities.\n\nWhat do you need to succeed?\n\nMust Have\n• Extensive experience in AI/ML development and deployment, demonstrating a deep understanding of machine learning algorithms, models, and framework.\n• Proven expertise in MLOps, including the development and integration of MLOps platforms and technologies to automate the delivery of AI/ML at scale.\n• Strong proficiency in programming languages such as Python or Java, and experience with machine learning frameworks and libraries.\n• Experience with containerization technologies such as Docker, Kubernetes, and OpenShift for efficient deployment and management of AI/ML applications\n• Strong technology skills and expertise, with a focus on current and emerging big-data technologies relevant to model development and deployment (Python, PySpark, SQL, Docker, Dagster, Spark, S3, Trino, Tableau, classification models, propensity models, timeseries models, NLP, LLMs, neural networks, etc.).\n• Deep understanding of business context, objectives, and requirements. Ability to align ML solutions with business goals, identify opportunities for ML applications, and communicate the value and potential impact to the organization.\n• Excellent problem-solving skills and the ability to think critically and creatively.\n• Strong communication and presentation skills, with the ability to explain complex concepts to both technical and non-technical stakeholders.\n\nNice to Have\n• Bachelor's or Master's degree in Computer Science, Engineering, or a related field.\n• Demonstrated success in applying agile best-practices to frame problems and prioritize key outcomes; hypothesize, iterate, and continuously improve on solutions; and continuously deliver incremental value to end-users and key stakeholders.\n• Previous experience in the wealth and asset management industry.\n\nWhat’s in it for you?\n\nWe thrive on the challenge to be our best, progressive thinking to keep growing, and working together to deliver trusted advice to help our clients thrive and communities prosper. We care about each other, reaching our potential, making a difference to our communities, and achieving success that is mutual.\n• Opportunity to build cross platform experience – in a high growth strategic segment.\n• Opportunity to work with a strategic client segment and experience in unique / customized lending.\n• Opportunity to work with senior leaders across RBC including Wealth Management, Canadian Banking and Capital Markets.\n• A comprehensive Total Rewards Program including bonuses and flexible benefits, competitive compensation, commissions, and stock where applicable.\n• Leaders who support your development through coaching and managing opportunities.\n• Flexible work/life balance options.\n• Access to a variety of job opportunities across business and geographies.\n\nJob Skills\nBig Data Management, Cloud Computing, Database Development, Data Mining, Data Warehousing (DW), ETL Processing, Problem Solving, Quality Management, Requirements Analysis\n\nAdditional Job Details\n\nAddress:\n\nRBC CENTRE, 155 WELLINGTON ST W:TORONTO\n\nCity:\n\nTORONTO\n\nCountry:\n\nCanada\n\nWork hours/week:\n\n37.5\n\nEmployment Type:\n\nFull time\n\nPlatform:\n\nWealth Management\n\nJob Type:\n\nRegular\n\nPay Type:\n\nSalaried\n\nPosted Date:\n\n2024-01-10\n\nApplication Deadline:\n\n2024-01-28\n\nInclusion and Equal Opportunity Employment\n\nAt RBC, we embrace diversity and inclusion for innovation and growth. We are committed to building inclusive teams and an equitable workplace for our employees to bring their true selves to work. We are taking actions to tackle issues of inequity and systemic bias to support our diverse talent, clients and communities.\n\u200b\u200b\u200b\u200b\u200b\u200b\u200b\nWe also strive to provide an accessible candidate experience for our prospective employees with different abilities. Please let us know if you need any accommodations during the recruitment process.\n\nJoin our Talent Community\n\nStay in-the-know about great career opportunities at RBC. Sign up and get customized info on our latest jobs, career tips and Recruitment events that matter to you.\n\nExpand your limits and create a new future together at RBC. Find out how we use our passion and drive to enhance the well-being of our clients and communities at jobs.rbc.com"
                ]
            }
        ],
        "relatedLinks": [
            {"link": "http://www.rbc.com/", "text": "rbc.com"},
            {
                "link": "https://www.google.com/search?sca_esv=600122311&q=Royal+Bank+of+Canada&sa=X&ved=0ahUKEwisrrCM-OyDAxXZj2oFHQAUACwQmJACCMEO",
                "text": "See web results for Royal Bank of Canada",
            },
        ],
        "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ89EMaFYiiHBxj4jEF-0jW1cZ73A2o7hPQ3oHL&s=0",
        "extras": ["22 hours ago", "Full-time"],
        "metadata": {"postedAt": "22 hours ago", "scheduleType": "Full-time"},
        "applyLink": {
            "title": "Apply on RBC Careers",
            "link": "https://jobs.rbc.com/ca/en/job/R-0000075808/Principal-Engineer-AI-Machine-Learning?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic",
        },
    }

    parsed_jd = chat.parse(json_jd=sample_jd, json_parsed_sample=json_parsed_sample)
    print(type(parsed_jd), "\n", parsed_jd)
