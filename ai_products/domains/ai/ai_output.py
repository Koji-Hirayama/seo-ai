from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class AiOutput:
    output: str
    output_model: Dict
    token: int
    cost: float
    response_date: datetime
    is_error: bool
