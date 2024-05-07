from pydantic import BaseModel
from ai_products.domains.ai.output_example_model import OutputExampleModel
from ai_products.integrations.llm.chat_open_ai import ChatOpenAi
from ai_products.models import AiModel
from ai_products.services.ai.interface.ai_service_interface import (
    AiAnswer,
    AiServiceInterface,
)
from ai_products.services.ai.messages.get_scraping_prompt_message_service import (
    GetScrapingPromptMessageService,
)
from ai_products.services.ai.serializers.ai_output_converter_service import (
    AiOutputConverterService,
)
from utils.errors import CustomApiErrorException


class ScrapingPromptAiService(AiServiceInterface):
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

    def ai_answer(self, ai_model: AiModel) -> AiAnswer:
        scraping_prompt_service = GetScrapingPromptMessageService()
        human_message = scraping_prompt_service.get_human_message(
            input=self.input, urls=self.urls
        )

        messages = [
            human_message,
        ]
        function = {
            "name": "answer_to_prompt",
            "description": self.output_example_model_description,
            "parameters": self.output_model_class.model_json_schema(),
        }
        try:
            llm = ChatOpenAi(ai_model=ai_model)
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
