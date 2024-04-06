from abc import ABC, abstractmethod
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from dataclasses import dataclass


class OutputExampleModelKey(BaseModel):
    key: str
    description: str
    examples: List[str]
    type: str


class OutputExampleModel(BaseModel):
    keys: List[OutputExampleModelKey]


@dataclass
class AiAnswer:
    prompt: str
    output: str
    output_model: Dict
    is_error: bool


@dataclass
class AiPrompt:
    prompt: str
    output_example_model_description: str
    output_example_model: OutputExampleModel
    token: int
    cost: float
    request_date: datetime


@dataclass
class AiOutput:
    output: str
    output_model: Dict
    token: int
    cost: float
    response_date: datetime
    is_error: bool


@dataclass
class Ai:
    ai_prompt: AiPrompt
    ai_output: AiOutput
    total_token: int
    total_cost: float


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
    def ai_answer(self) -> AiAnswer:
        pass
