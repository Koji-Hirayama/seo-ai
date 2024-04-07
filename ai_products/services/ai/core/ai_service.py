from pydantic import BaseModel
from ai_products.integrations.llm.simple_llm_service import SimpleLlmService
from ai_products.models import Prompt, PromptOutput, User
from utils.errors import CustomApiErrorException
from ..interface.ai_logic_service_interface import (
    Ai,
    AiOutput,
    AiPrompt,
    AiLogicServiceInterface,
)
from langchain_community.callbacks import get_openai_callback
from django.utils import timezone
from ai_products.services.prompt_output.create_prompt_output_service import (
    CreatePromptOutputService,
)
from ai_products.services.prompt.create_prompt_service import CreatePromptService
from dataclasses import dataclass
from django.db import transaction
from utils.errors import CustomApiErrorException


@dataclass
class AiAnswerResults:
    answer: Ai
    prompt: Prompt
    prompt_output: PromptOutput


class AiService:
    def __init__(self, ai_service: AiLogicServiceInterface):
        self._ai_service = ai_service
        self._output_example_model_description = (
            self._ai_service.output_example_model_description
        )
        self._output_example_model = self._ai_service.output_example_model

    def ai_answer(self) -> Ai:

        with get_openai_callback() as cb:
            ai_request_date = timezone.localtime(timezone.now())
            answer = self._ai_service.ai_answer()
            ai_response_date = timezone.localtime(timezone.now())

            ai_prompt = AiPrompt(
                prompt=answer.prompt,
                output_example_model_description=self._output_example_model_description,
                output_example_model=self._output_example_model,
                token=cb.prompt_tokens,
                # プロンプトのトークンのコスト計算
                cost=(
                    cb.total_cost * (cb.prompt_tokens / cb.total_tokens)
                    if cb.total_cost != 0
                    else 0
                ),
                request_date=ai_request_date,
            )

            ai_output = AiOutput(
                output=answer.output,
                output_model=answer.output_model,
                token=cb.completion_tokens,
                # AIのトークンのコスト計算
                cost=(
                    cb.total_cost * (cb.completion_tokens / cb.total_tokens)
                    if cb.total_cost != 0
                    else 0
                ),
                response_date=ai_response_date,
                is_error=answer.is_error,
            )

            ai = Ai(
                ai_prompt=ai_prompt,
                ai_output=ai_output,
                total_cost=cb.total_cost,
                total_token=cb.total_tokens,
            )

            return ai

    def save_ai_answer(
        self, work_id: int, ai_model_id: int, user: User, order: int
    ) -> AiAnswerResults:
        answer: Ai = self.ai_answer()
        create_prompt_service = CreatePromptService()
        create_output_service = CreatePromptOutputService()
        with transaction.atomic():
            try:
                prompt: Prompt = create_prompt_service.create_prompt(
                    prompt=answer.ai_prompt.prompt,
                    output_example_model_description=answer.ai_prompt.output_example_model_description,
                    output_example_model=answer.ai_prompt.output_example_model.model_dump(),
                    request_date=answer.ai_prompt.request_date,
                    token=answer.ai_prompt.token,
                    cost=answer.ai_prompt.cost,
                    total_cost=answer.total_cost,
                    work_id=work_id,
                    ai_model_id=ai_model_id,
                    user=user,
                    order=order,
                )

                prompt_output: PromptOutput = (
                    create_output_service.create_prompt_output(
                        output=answer.ai_output.output,
                        output_model=answer.ai_output.output_model,
                        response_date=answer.ai_output.response_date,
                        prompt_id=prompt.id,
                        token=answer.ai_output.token,
                        cost=answer.ai_output.cost,
                        total_cost=answer.total_cost,
                        user=user,
                        order=order,
                        is_error=answer.ai_output.is_error,
                    )
                )
            except CustomApiErrorException as e:
                raise e

        return AiAnswerResults(
            answer=answer, prompt=prompt, prompt_output=prompt_output
        )
