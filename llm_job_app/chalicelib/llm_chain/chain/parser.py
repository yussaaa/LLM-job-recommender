from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate

import ast


class ParserLLM:
    """
    A class that represents a parser for LLM (Language Model) chains.

    Args:
        model (str): The name of the language model to use. Default is "gpt-3.5-turbo-1106".
        temperature (float): The temperature parameter for generating responses. Default is 0.1.
        max_tokens (int): The maximum number of tokens allowed in the generated response. Default is 3000.
        **kwargs: Additional keyword arguments to be passed to the underlying ChatOpenAI instance.

    Attributes:
        model (str): The name of the language model being used.
        temperature (float): The temperature parameter for generating responses.
        max_tokens (int): The maximum number of tokens allowed in the generated response.
        chat (ChatOpenAI): The ChatOpenAI instance used for generating responses.

    Methods:
        run_chain(chain, json_sample_schema, json_input):
            Runs the LLM chain with the given JSON sample schema and input data.

        parse(json_input, json_sample_schema):
            Parses the given JSON input using the LLM chain.

    """

    def __init__(
        self, model="gpt-3.5-turbo-1106", temperature=0.1, max_tokens=3000, **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.chat = self.__init_llm()

    def __init_llm(self):
        """
        Initializes the ChatOpenAI instance for generating responses.

        Returns:
            ChatOpenAI: The initialized ChatOpenAI instance.
        """
        return ChatOpenAI(
            model=self.model, temperature=self.temperature, max_tokens=self.max_tokens
        )

    def run_chain(self, chain, json_sample_schema, json_input):
        """
        Runs the LLM chain with the given JSON sample schema and input data.

        Args:
            chain (LLMChain): The LLMChain instance representing the chain to be run.
            json_sample_schema (str): The JSON sample schema.
            json_input (str): The JSON input data.

        Returns:
            str: The parsed data as a string.
        """
        return chain.run(json_sample_schema=json_sample_schema, json=json_input)

    def parse(self, json_input, json_sample_schema):
        """
        Parses the given JSON input using the LLM chain.

        Args:
            json_input (str): The JSON input data.
            json_sample_schema (str): The JSON sample schema.

        Returns:
            dict: The parsed data as a dictionary.
        """
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
