from typing import List
from .base_ai_request_input_data import BaseAiRequestInputData


class ScrapingPrompt(BaseAiRequestInputData):
    urls: List[str]
    input: str
