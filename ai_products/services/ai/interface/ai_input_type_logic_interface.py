from abc import ABC, abstractmethod
from ai_products.domains.ai.ai_input_type_logic_result import AiInputTypeLogicResult
from ai_products.domains.ai.ai_request_data.ai_request_input_data_type import (
    AiRequestInputDataType,
)
from ai_products.models import AiInput


class AiInputTypeLogicInterface(ABC):

    @abstractmethod
    def result(
        self, ai_input: AiInput, input_data: AiRequestInputDataType
    ) -> AiInputTypeLogicResult:
        pass
