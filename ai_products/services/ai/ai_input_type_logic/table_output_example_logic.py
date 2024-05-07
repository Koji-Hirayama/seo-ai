from ai_products.domains.ai.ai_request_data.table_output_example import (
    TableOutputExample,
)
from ai_products.domains.ai.output_example_model import OutputExampleModel
from ai_products.serializers.ai.utils.dynamic_pydantic_model_serializer import (
    AiOutputPydanticModelSerialiser,
)
from ai_products.services.ai.interface.ai_input_type_logic_interface import (
    AiInputTypeLogicInterface,
    AiInputTypeLogicResult,
)
from ai_products.models import AiInput, AiInputField, PromptInput
from typing import List
from utils.errors import CustomApiErrorException


class TableOutputExampleLogic(AiInputTypeLogicInterface):

    def result(
        self, ai_input: AiInput, input_data: TableOutputExample
    ) -> AiInputTypeLogicResult:
        aiOutputPydanticModelserialiser = AiOutputPydanticModelSerialiser()
        try:
            output_base_model = aiOutputPydanticModelserialiser.create_base_model(
                input_data.output_example_model.model_dump()
            )
        except CustomApiErrorException as e:
            raise e
        # ai_input_typeがTableOutputExampleの場合
        function = {
            "name": "answer_to_prompt",
            "description": input_data.output_example_model_description,
            "parameters": output_base_model.model_json_schema(),
        }
        ai_input_field: AiInputField = ai_input.get_ai_input_field_by_field_type_id(3)
        # AI回答スキーマ設定のpromptInputとResultsを作成
        inputs = self.create_table_output_example_prompt_inputs(
            ai_input_id=ai_input.id,
            ai_input_field_id=ai_input_field.id,
            description=input_data.output_example_model_description,
            example_model=input_data.output_example_model,
        )
        return AiInputTypeLogicResult(
            function=function, output_base_model=output_base_model, prompt_inputs=inputs
        )

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
