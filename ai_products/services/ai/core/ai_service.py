from ai_products.domains.ai.ai import Ai
from ai_products.domains.ai.ai_answer_results import AiAnswerResults
from ai_products.domains.ai.ai_output import AiOutput
from ai_products.domains.ai.ai_prompt import AiPrompt
from ai_products.domains.ai.ai_request_data.ai_request_data import AiRequestData
from ai_products.domains.ai.ai_request_params import AiRequestParams
from ai_products.models import (
    Prompt,
    PromptOutput,
    User,
    AiModel,
    PromptInput,
    AiRequest,
)
from ai_products.services.ai_model.get_ai_models_service import GetAiModelService
from ai_products.services.ai_request.create_ai_request_service import (
    CreateAiRequestService,
)
from ai_products.services.ai_type_ai_input.get_ai_type_input_fields_service import (
    GetAiTypeInputFieldsService,
)
from ai_products.services.prompt.create_prompt_service import CreatePromptService
from ai_products.services.prompt_input.create_prompt_input_service import (
    CreatePromptInputService,
)
from ai_products.services.prompt_input.get_prompt_input_service import (
    GetPromptInputService,
)
from ai_products.services.work.get_work_service import GetWorkService
from utils.errors import CustomApiErrorException
from utils.errors.error_type import ErrorType
from ..interface.ai_service_interface import (
    AiAnswer,
    AiServiceInterface,
)
from langchain_community.callbacks import get_openai_callback
from django.utils import timezone
from ai_products.services.prompt_output.create_prompt_output_service import (
    CreatePromptOutputService,
)
from django.db import transaction
from django.db.models.query import QuerySet


class AiService:
    def __init__(
        self,
        ai_service: AiServiceInterface,
        params: AiRequestParams,
    ):
        self._ai_service = ai_service
        self._params = params

    def ai_answer(self) -> Ai:
        # AiTypeのinputfieldのデータ取得
        get_ai_type_ai_input_fields_service = GetAiTypeInputFieldsService()
        ai_type_ai_inputs = (
            get_ai_type_ai_input_fields_service.get_ai_type_input_fields(
                ai_type_id=self._params.ai_type_id
            )
        )

        # 一旦、AIの連結概念がまだないので、配列の先頭を直取りする
        ai_request_data: AiRequestData = self._params.request_data.ai_request_datas[0]

        # AiModel取得
        get_ai_model_service = GetAiModelService()
        ai_model: AiModel = get_ai_model_service.get_ai_model(
            id=ai_request_data.ai_model_id
        )

        with get_openai_callback() as cb:
            ai_request_date = timezone.localtime(timezone.now())
            try:
                answer: AiAnswer = self._ai_service.ai_answer(
                    ai_model=ai_model,
                    ai_type_ai_inputs=ai_type_ai_inputs,
                    ai_request_data=ai_request_data,
                )
            except CustomApiErrorException as e:
                raise e
            ai_response_date = timezone.localtime(timezone.now())

            output_example_data = ai_request_data.get_table_output_example_input_data()
            # 以下、一旦
            if output_example_data == None:
                raise CustomApiErrorException(
                    error_type=ErrorType.AI_REQUEST_INPUT_DATA_NOT_FOUND,
                    message="TableOutputExampleが見つかりませんでした。",
                )

            ai_prompt = AiPrompt(
                prompt=answer.prompt,
                output_example_model_description=output_example_data.output_example_model_description,
                output_example_model=output_example_data.output_example_model,
                token=cb.prompt_tokens,
                # プロンプトのトークンのコスト計算
                cost=self.calculate_cost_per_token(
                    total_cost=cb.total_cost,
                    completion_tokens=cb.prompt_tokens,
                    total_tokens=cb.total_tokens,
                ),
                request_date=ai_request_date,
            )

            ai_output = AiOutput(
                output=answer.output,
                output_model=answer.output_model,
                token=cb.completion_tokens,
                # AIのトークンのコスト計算
                cost=self.calculate_cost_per_token(
                    total_cost=cb.total_cost,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
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
                prompt_inputs=answer.prompt_inputs,
            )

            return ai

    # TODO: おそらく後で複数aiを保存できる様にする
    def save(self, ai: Ai, user: User) -> AiAnswerResults:
        get_work_service = GetWorkService()
        create_ai_request_service = CreateAiRequestService()
        create_prompt_service = CreatePromptService()
        create_output_service = CreatePromptOutputService()
        create_prompt_input_service = CreatePromptInputService()
        get_prompt_input_service = GetPromptInputService()
        with transaction.atomic():
            try:
                work = get_work_service.get_work(id=self._params.work_id)

                create_ai_request: AiRequest = (
                    create_ai_request_service.create_ai_request(
                        task=work.task,
                        work=work,
                        user=user,
                        request_data=self._params.request_data.model_dump(),
                        status=0,
                    )
                )
                create_prompt: Prompt = create_prompt_service.create_prompt(
                    prompt=ai.ai_prompt.prompt,
                    output_example_model_description=ai.ai_prompt.output_example_model_description,
                    output_example_model=ai.ai_prompt.output_example_model.model_dump(),
                    request_date=ai.ai_prompt.request_date,
                    token=ai.ai_prompt.token,
                    cost=ai.ai_prompt.cost,
                    total_cost=ai.total_cost,
                    ai_request=create_ai_request,
                    work=work,
                    ai_model=ai.ai_model,
                    user=user,
                    order=1,
                )

                create_prompt_output: PromptOutput = (
                    create_output_service.create_prompt_output(
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

                # PromptInputリストを完成させる
                for prompt_input in ai.prompt_inputs:
                    prompt_input.prompt = create_prompt
                # PromptInput保存
                create_prompt_input_service.create_prompt_inputs(ai.prompt_inputs)
                # 保存したPromptInputを取得
                prompt_inputs: QuerySet[PromptInput] = (
                    get_prompt_input_service.get_prompt_inputs_by_prompt_id(
                        prompt_id=create_prompt.id
                    )
                )

            except CustomApiErrorException as e:
                raise e

        return AiAnswerResults(
            ai=ai,
            ai_request=create_ai_request,
            prompt=create_prompt,
            prompt_output=create_prompt_output,
            prompt_inputs=prompt_inputs,
        )

    def save_ai_answer(self, user: User) -> AiAnswerResults:
        try:
            ai: Ai = self.ai_answer()
            results: AiAnswerResults = self.save(ai=ai, user=user)
        except CustomApiErrorException as e:
            raise e
        return results

    def calculate_cost_per_token(self, total_cost, completion_tokens, total_tokens):
        """
        トークン一つ当たりのコストを計算します。

        Args:
            total_cost (float): トータルコスト
            completion_tokens (int): 完了したトークンの数
            total_tokens (int): トータルトークンの数

        Returns:
            float: token一つ当たりのコスト
        """
        if total_tokens == 0:
            return 0  # 0除算を防ぐため
        cost_per_token = total_cost * (completion_tokens / total_tokens)
        return cost_per_token
