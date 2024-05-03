from ai_products.models import AiInput
from ai_products.serializers.ai.utils.ai_serializer import AiRequestPrams
from ai_products.services.ai.ai_input_type_logic.scraping_prompt_logic import (
    ScrapingPromptLogic,
)
from ai_products.services.ai.ai_input_type_logic.table_output_example_logic import (
    TableOutputExampleLogic,
)
from ai_products.services.ai.interface.ai_input_type_logic_interface import (
    AiInputTypeLogicInterface,
    AiInputTypeLogicResult,
)
from typing import Dict


class AiInputTypeLogicService:
    # TODO: ai_input以外のパラメータを効率的に受け取る仕組みを作る必要あり
    def __init__(self, ai_input: AiInput, params: AiRequestPrams):
        self._ai_input = ai_input

        self._ai_input_type_logic_dict: Dict[int, AiInputTypeLogicInterface] = {
            1: ScrapingPromptLogic(
                ai_input=ai_input, urls=params.urls, user_input=params.prompt_user_input
            ),
            2: TableOutputExampleLogic(
                ai_input=ai_input,
                output_example_model_description=params.output_example_model_description,
                output_example_model=params.output_example_model,
                output_model_class=params.output_model_class,
            ),
        }

    def result(self) -> AiInputTypeLogicResult:
        logic = self._ai_input_type_logic_dict[self._ai_input.ai_input_type.id]
        return logic.result()
