from dataclasses import dataclass
from datetime import datetime
from ai_products.domains.ai.output_example_model import OutputExampleModel


@dataclass
class AiPrompt:
    prompt: str
    output_example_model_description: str
    output_example_model: OutputExampleModel
    token: int
    cost: float
    request_date: datetime
