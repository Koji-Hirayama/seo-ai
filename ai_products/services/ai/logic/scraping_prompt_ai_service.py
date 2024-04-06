from typing import List
from pydantic import BaseModel
from ai_products.integrations.llm.chat_open_ai import ChatOpenAi
from ai_products.integrations.llm.simple_llm_answers.simple_llm_answer_with_function_calling import (
    SimpleLlmAnswerWithFunctionCalling,
)
from ai_products.services.ai.interface.ai_logic_service_interface import (
    AiAnswer,
    AiLogicServiceInterface,
    OutputExampleModel,
)
from ai_products.services.ai.serializers.ai_output_converter_service import (
    AiOutputConverterService,
)
from utils.errors import CustomApiErrorException
from ..scraping.unstructured_url_loader_service import UnstructuredURLLoaderService
from langchain.schema import HumanMessage
from utils.errors import CustomApiErrorException


class ScrapingPromptAiService(AiLogicServiceInterface):
    def __init__(
        self,
        output_example_model_description: str,
        output_example_model: OutputExampleModel,
        output_model_class: BaseModel,
        **kwargs,
    ):
        super().__init__(
            output_example_model_description,
            output_example_model,
            output_model_class,
            **kwargs,
        )
        self.input = kwargs.get("input")
        self.urls = kwargs.get("urls")

    def ai_answer(self) -> AiAnswer:
        scraping = UnstructuredURLLoaderService()
        scraping_datas = scraping.url_loader(self.urls)
        context = ""
        for data in scraping_datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            context += text + "\n\n" + "=======================" + "\n\n"
        PROMPT_TEMPLETE = """次のコンテキストから{input}\n
        {context}
        """
        messages = [
            HumanMessage(
                content=PROMPT_TEMPLETE.format(context=context, input=self.input)
            )
        ]
        function = {
            "name": "answer_to_prompt",
            "description": self.output_example_model_description,
            "parameters": self.output_model_class.model_json_schema(),
        }

        try:
            llm = ChatOpenAi(model_name="gpt-3.5-turbo-1106")
            result = llm.function_call_predict_messages(
                messages=messages, functions=[function]
            )
            converter_service = AiOutputConverterService()
            output_model = converter_service.function_call_arguments_to_dict(
                additional_kwargs=result.additional_kwargs,
                output_model_class=self.output_model_class,
            )
        except CustomApiErrorException as e:
            return AiAnswer(
                prompt=messages[0].content,
                output="",
                output_model=e.get_error(),
                is_error=True,
            )

        return AiAnswer(
            prompt=messages[0].content,
            output="",
            output_model=output_model,
            is_error=False,
        )
