from abc import ABC, abstractmethod
from ai_products.models import AiInput
from dataclasses import dataclass, field
from ai_products.models import AiInput, PromptInput
from typing import Dict, Any, List, Optional


@dataclass
class AiInputTypeLogicResult:
    message: Optional[str] = None
    function: Optional[Dict[str, Any]] = None
    prompt_inputs: List[PromptInput] = field(default_factory=list)


class AiInputTypeLogicInterface(ABC):

    def __init__(self, ai_input: AiInput):
        self.ai_input = ai_input

    @abstractmethod
    def result(self) -> AiInputTypeLogicResult:
        pass
