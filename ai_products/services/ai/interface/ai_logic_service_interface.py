from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel
from dataclasses import dataclass
from ai_products.models import AiModel


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
    output: str
    output_model: Dict
    is_error: bool


class AiLogicServiceInterface(ABC):
    @abstractmethod
    def __init__(
        self,
        output_example_model_description: str,
        output_example_model: OutputExampleModel,
        output_model_class: BaseModel,
        **kwargs
    ):
        self.output_example_model_description = output_example_model_description
        self.output_example_model = output_example_model
        self.output_model_class = output_model_class

    @abstractmethod
    def ai_answer(self, ai_model: AiModel) -> AiAnswer:
        pass
