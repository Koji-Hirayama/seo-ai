from pydantic import BaseModel
from ai_products.integrations.llm.simple_llm_service import SimpleLlmService
from ai_products.models import Prompt, PromptOutput, User, AiModel, Work
from ai_products.services.ai_model.get_ai_models_service import GetAiModelService
from ai_products.services.work.create_work_service import CreateWorkService
from utils.errors import CustomApiErrorException
from ..interface.ai_logic_service_interface import (
    AiLogicServiceInterface,
    OutputExampleModel,
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
from datetime import datetime
from typing import Dict


@dataclass
class AiPrompt:
    prompt: str
    output_example_model_description: str
    output_example_model: OutputExampleModel
    token: int
    cost: float
    request_date: datetime


@dataclass
class AiOutput:
    output: str
    output_model: Dict
    token: int
    cost: float
    response_date: datetime
    is_error: bool


@dataclass
class _AiModel:
    id: int
    name: str


@dataclass
class Ai:
    ai_prompt: AiPrompt
    ai_output: AiOutput
    total_token: int
    total_cost: float
    ai_model: _AiModel


@dataclass
class AiAnswerResults:
    ai: Ai
    prompt: Prompt
    prompt_output: PromptOutput
    work: Work


class AiService:
    def __init__(self, ai_model_id: int, ai_logic_service: AiLogicServiceInterface):
        self._ai_logic_service = ai_logic_service
        self._output_example_model_description = (
            self._ai_logic_service.output_example_model_description
        )
        self._output_example_model = self._ai_logic_service.output_example_model
        self.ai_model_id = ai_model_id

    def ai_answer(self) -> Ai:
        get_ai_model_service = GetAiModelService()
        ai_model: _AiModel = get_ai_model_service.get_ai_model(id=self.ai_model_id)
        with get_openai_callback() as cb:
            ai_request_date = timezone.localtime(timezone.now())
            answer = self._ai_logic_service.ai_answer(ai_model=ai_model)
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
                ai_model=ai_model,
                ai_prompt=ai_prompt,
                ai_output=ai_output,
                total_cost=cb.total_cost,
                total_token=cb.total_tokens,
            )

            return ai

    # TODO: おそらく後で複数aiを保存できる様にする
    def save(self, ai: Ai, user: User, task_id: int) -> AiAnswerResults:
        create_work_service = CreateWorkService()
        create_prompt_service = CreatePromptService()
        create_output_service = CreatePromptOutputService()
        with transaction.atomic():
            try:
                create_work = create_work_service.create_work(task_id=task_id)
                create_prompt: Prompt = create_prompt_service.create_prompt_direct(
                    prompt=ai.ai_prompt.prompt,
                    output_example_model_description=ai.ai_prompt.output_example_model_description,
                    output_example_model=ai.ai_prompt.output_example_model.model_dump(),
                    request_date=ai.ai_prompt.request_date,
                    token=ai.ai_prompt.token,
                    cost=ai.ai_prompt.cost,
                    total_cost=ai.total_cost,
                    work=create_work,
                    ai_model=AiModel(id=ai.ai_model.id, name=ai.ai_model.name),
                    user=user,
                    order=1,
                )

                create_prompt_output: PromptOutput = (
                    create_output_service.create_prompt_output_direct(
                        output=ai.ai_output.output,
                        output_model=ai.ai_output.output_model,
                        response_date=ai.ai_output.response_date,
                        prompt=create_prompt,
                        token=ai.ai_output.token,
                        cost=ai.ai_output.cost,
                        total_cost=ai.total_cost,
                        user=user,
                        order=1,
                        is_error=ai.ai_output.is_error,
                    )
                )
            except CustomApiErrorException as e:
                raise e

        return AiAnswerResults(
            ai=ai,
            prompt=create_prompt,
            prompt_output=create_prompt_output,
            work=create_work,
        )

    def save_ai_answer(self, user: User, task_id: int) -> AiAnswerResults:
        ai: Ai = self.ai_answer()
        try:
            results: AiAnswerResults = self.save(ai=ai, user=user, task_id=task_id)
        except CustomApiErrorException as e:
            raise e
        return results
