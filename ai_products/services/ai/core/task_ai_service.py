from ai_products.models import AiModel, PromptInput, AiInput, AiTypeAiInput
from ai_products.services.ai.ai_input_type_logic.ai_input_type_logic_service import (
    AiInputTypeLogicService,
)
from ai_products.services.ai.interface.ai_service_interface import (
    AiAnswer,
    AiServiceInterface,
)
from ai_products.integrations.llm.chat_open_ai import ChatOpenAi
from utils.errors import CustomApiErrorException
from ai_products.services.ai.serializers.ai_output_converter_service import (
    AiOutputConverterService,
)
from typing import List, Dict, Any
from ai_products.serializers.ai.utils.ai_serializer import AiRequestPrams
from langchain.schema import HumanMessage, AIMessage, SystemMessage


class TaskAiService(AiServiceInterface):

    def ai_answer(
        self,
        ai_model: AiModel,
        ai_type_ai_inputs: List[AiTypeAiInput],
        params: AiRequestPrams,
    ) -> AiAnswer:
        messages: List[SystemMessage | HumanMessage | AIMessage] = []
        functions: List[Dict[str, Any]] = []
        prompt_inputs: List[PromptInput] = []
        for ai_type_ai_input in ai_type_ai_inputs:
            ai_input: AiInput = ai_type_ai_input.ai_input
            logic_service = AiInputTypeLogicService(ai_input=ai_input, params=params)
            result = logic_service.result()
            if result.message is not None:
                messages.append(HumanMessage(content=result.message))
            if result.function is not None:
                functions.append(result.function)
            prompt_inputs = prompt_inputs + result.prompt_inputs

        if functions != []:
            try:
                llm = ChatOpenAi(ai_model=ai_model)
                result = llm.function_call_predict_messages(
                    messages=messages, functions=functions
                )
                converter_service = AiOutputConverterService()
                output_model = converter_service.function_call_arguments_to_dict(
                    additional_kwargs=result.additional_kwargs,
                    output_model_class=params.output_model_class,
                )
            except CustomApiErrorException as e:
                return AiAnswer(
                    prompt=messages[0].content,
                    output="",
                    output_model=e.get_error(),
                    is_error=True,
                )

            return AiAnswer(
                prompt=messages[0].content,
                prompt_inputs=prompt_inputs,
                output="",
                output_model=output_model,
                is_error=False,
            )
        else:
            # ファンクションコーリングではない場合
            # 一旦保留
            pass
