from dataclasses import dataclass
from typing import List, Dict
from ai_products.models import PromptInput


@dataclass
class AiAnswer:
    prompt: str
    prompt_inputs: List[PromptInput]
    output: str
    output_model: Dict
    is_error: bool
