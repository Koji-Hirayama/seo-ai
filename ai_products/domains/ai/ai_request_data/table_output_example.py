from ai_products.domains.ai.output_example_model import OutputExampleModel
from .base_ai_request_input_data import BaseAiRequestInputData


class TableOutputExample(BaseAiRequestInputData):
    output_example_model_description: str
    output_example_model: OutputExampleModel
