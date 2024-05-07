from dataclasses import dataclass
from typing import List
from ai_products.domains.ai.ai_output import AiOutput
from ai_products.domains.ai.ai_prompt import AiPrompt
from ai_products.models import PromptInput, AiModel


@dataclass
class Ai:
    ai_prompt: AiPrompt
    ai_output: AiOutput
    total_token: int
    total_cost: float
    ai_model: AiModel
    prompt_inputs: List[PromptInput]
