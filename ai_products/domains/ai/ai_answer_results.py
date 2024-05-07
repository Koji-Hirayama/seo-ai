from dataclasses import dataclass
from typing import List
from ai_products.domains.ai.ai import Ai
from ai_products.models import PromptInput, PromptOutput, Prompt, AiRequest


@dataclass
class AiAnswerResults:
    ai: Ai
    ai_request: AiRequest
    prompt: Prompt
    prompt_output: PromptOutput
    prompt_inputs: List[PromptInput]
