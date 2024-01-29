from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

import ast


class ParserLLM:
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

    def run_chain(self, chain, json_sample_schema, json_input):
        return chain.run(json_sample_schema=json_sample_schema, json=json_input)

    def parse(self, json_input, json_sample_schema):
        system_message_prompt = self.get_system_message_prompt(json_sample_schema)
        human_message_prompt = self.get_human_message_prompt(json_input)
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        chain = LLMChain(llm=self.chat, prompt=chat_prompt_template)

        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                parsed_data = self.run_chain(chain, json_sample_schema, json_input)
                data_dict = ast.literal_eval(parsed_data)
                return data_dict
            except Exception as e:
                attempts += 1
                print("----------------------------------------")
                print(f"Attempt {attempts} failed with error: {e}")
                if attempts < max_attempts:
                    print("Retrying...")
                else:
                    print("Max attempts reached. Handling error.")
                    print(f"When processing this data: \n{json_input}")
                    print("----------------------------------------")
