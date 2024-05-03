from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel
from dataclasses import dataclass
from ai_products.models import PromptInput


class OutputExampleModelKey(BaseModel):
    key: str
    description: str
    examples: List[Any]
    type: str


class OutputExampleModel(BaseModel):
    keys: List[OutputExampleModelKey]


@dataclass
class AiAnswer:
    prompt: str
    prompt_inputs: List[PromptInput]
    output: str
    output_model: Dict
    is_error: bool


class AiServiceInterface(ABC):

    @abstractmethod
    def ai_answer(
        self,
        ai_model,
        ai_type_ai_inputs,
        params,
    ) -> AiAnswer:
        pass
