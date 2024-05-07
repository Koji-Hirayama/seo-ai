from ai_products.domains.ai.ai_request_data.ai_request_data import AiRequestData
from ai_products.domains.ai.ai_request_params import AiRequestParams
from ai_products.models import AiInput
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
from utils.errors import CustomApiErrorException, ErrorDetail, ErrorType


class AiInputTypeLogicService:
    def __init__(self, ai_input: AiInput, ai_request_data: AiRequestData):
        self._ai_input = ai_input
        self._ai_request_data = ai_request_data
        self._ai_input_type_logic_dict: Dict[int, AiInputTypeLogicInterface] = {
            1: ScrapingPromptLogic(),
            2: TableOutputExampleLogic(),
        }

    def result(self) -> AiInputTypeLogicResult:
        try:
            logic = self._ai_input_type_logic_dict[self._ai_input.ai_input_type.id]
        except CustomApiErrorException as e:
            raise e

        ai_request_input_data = self._ai_request_data.get_input_data(
            ai_input_id=self._ai_input.id
        )
        if ai_request_input_data == None:
            raise CustomApiErrorException(
                error_type=ErrorType.AI_REQUEST_INPUT_DATA_NOT_FOUND,
                message=f"ai_input_idが{self._ai_input.id}のai_request_input_dataは存在しません。",
            )
        return logic.result(ai_input=self._ai_input, input_data=ai_request_input_data)
