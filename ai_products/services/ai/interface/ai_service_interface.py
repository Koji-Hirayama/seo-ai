from abc import ABC, abstractmethod
from ai_products.domains.ai.ai_answer import AiAnswer


class AiServiceInterface(ABC):

    @abstractmethod
    def ai_answer(
        self,
        ai_model,
        ai_type_ai_inputs,
        params,
    ) -> AiAnswer:
        pass
