from ai_products.services.ai.interface.ai_input_type_logic_interface import (
    AiInputTypeLogicInterface,
    AiInputTypeLogicResult,
)
from ai_products.services.ai.interface.ai_service_interface import OutputExampleModel
from ai_products.models import AiInput, AiInputField, PromptInput
from typing import List
from pydantic import BaseModel


class TableOutputExampleLogic(AiInputTypeLogicInterface):
    def __init__(
        self,
        ai_input: AiInput,
        output_example_model_description: str,
        output_example_model: OutputExampleModel,
        output_model_class: BaseModel,
    ):
        super().__init__(ai_input)
        self.output_example_model_description = output_example_model_description
        self.output_example_model = output_example_model
        self.output_model_class = output_model_class

    def result(self) -> AiInputTypeLogicResult:
        # ai_input_typeがTableOutputExampleの場合
        function = {
            "name": "answer_to_prompt",
            "description": self.output_example_model_description,
            "parameters": self.output_model_class.model_json_schema(),
        }
        ai_input_field: AiInputField = (
            self.ai_input.get_ai_input_field_by_field_type_id(3)
        )
        # AI回答スキーマ設定のpromptInputとResultsを作成
        inputs = self.create_table_output_example_prompt_inputs(
            ai_input_id=self.ai_input.id,
            ai_input_field_id=ai_input_field.id,
            description=self.output_example_model_description,
            example_model=self.output_example_model,
        )
        return AiInputTypeLogicResult(function=function, prompt_inputs=inputs)

    def create_table_output_example_prompt_inputs(
        self,
        ai_input_id,
        ai_input_field_id,
        description: str,
        example_model: OutputExampleModel,
    ) -> List[PromptInput]:
        prompt_inputs: List[PromptInput] = []

        prompt_input: PromptInput = PromptInput(
            output_example_model_description=description,
            output_example_model=example_model.model_dump_json(),
            ai_input_id=ai_input_id,
            ai_input_field_id=ai_input_field_id,
            result_json={
                "output_example_model_description": description,
                "output_example_model": example_model.model_dump_json(),
            },
        )
        prompt_inputs.append(prompt_input)

        return prompt_inputs
