from typing import List
from langchain_openai import ChatOpenAI
from utils.errors import OpenAIErrorHandler


class ChatOpenAi:
    def __init__(
        self, model_name: str = "gpt-3.5-turbo-1106", temperature: int = 0, n: int = 1
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.n = n

    def function_call_predict_messages(self, messages: List[any], functions: List[any]):
        llm = ChatOpenAI(
            model_name=self.model_name, temperature=self.temperature, n=self.n
        )
        try:
            result = llm.predict_messages(
                messages=messages,
                functions=functions,
            )
        except Exception as e:
            raise OpenAIErrorHandler.handle_error(e)
        return result
