from typing import List
from pydantic import BaseModel
from ai_products.domains.ai.output_example_key_model import OutputExampleKeyModel


class OutputExampleModel(BaseModel):
    keys: List[OutputExampleKeyModel]
