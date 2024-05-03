from ai_products.services.ai.interface.ai_input_type_logic_interface import (
    AiInputTypeLogicInterface,
    AiInputTypeLogicResult,
)
from ai_products.services.ai.messages.get_scraping_prompt_message_service import (
    GetScrapingPromptMessageService,
)
from ai_products.services.ai.scraping.get_scraping_results_service import (
    GetScrapingResultsService,
    ScrapingResult,
)

from ai_products.models import AiInput, AiInputField, PromptInput
from typing import List


class ScrapingPromptLogic(AiInputTypeLogicInterface):

    def __init__(
        self,
        ai_input: AiInput,
        urls: List[str],
        user_input: str,
    ):
        super().__init__(ai_input)
        self.urls = urls
        self.user_input = user_input

    def result(self) -> AiInputTypeLogicResult:
        # ①スクレイピング結果取得
        scraping_result_service = GetScrapingResultsService()
        scraping_results = scraping_result_service.get_results(self.urls)
        # スクレイピング結果のpromptInputとResultsを作成
        ai_input_field: AiInputField = (
            self.ai_input.get_ai_input_field_by_field_type_id(1)
        )
        scraping_inputs = self.create_scraping_results_prompt_inputs(
            ai_input_id=self.ai_input.id,
            ai_input_field_id=ai_input_field.id,
            scraping_results=scraping_results,
        )

        # ②取得したスクレイピング結果と指示文を元にプロンプト作成する。
        ai_input_field: AiInputField = (
            self.ai_input.get_ai_input_field_by_field_type_id(2)
        )
        scraping_prompt_message_service = GetScrapingPromptMessageService(
            context_input_field=ai_input_field,
            input=self.user_input,
        )
        message = scraping_prompt_message_service.get_scraping_result_injection_message(
            scraping_results=scraping_results
        )

        # 上記で作成されたプロンプトのpromptInputを作成
        prompt_inputs = self.create_scraping_result_injection_prompt_inputs(
            ai_input_id=self.ai_input.id,
            ai_input_field_id=ai_input_field.id,
            user_input=self.user_input,
            result_injection=scraping_prompt_message_service.join_scraping_results_as_text(
                scraping_results=scraping_results
            ),
            prompt=message,
        )
        inputs = scraping_inputs + prompt_inputs
        return AiInputTypeLogicResult(message=message, prompt_inputs=inputs)

    # ScrapingPromptのArrayShortTextFieldのPromptInputの作成。
    def create_scraping_results_prompt_inputs(
        self,
        ai_input_id: int,
        ai_input_field_id: int,
        scraping_results: List[ScrapingResult],
    ) -> List[PromptInput]:
        prompt_inputs: List[PromptInput] = []

        for scraping_result in scraping_results:
            prompt_input: PromptInput = PromptInput(
                input=scraping_result.url,
                ai_input_id=ai_input_id,
                ai_input_field_id=ai_input_field_id,
                result_json=scraping_result.model_dump_json(),
            )
            prompt_inputs.append(prompt_input)

        return prompt_inputs

    # ScrapingPromptのInteractiveResultInjectionFieldのPromptInputの作成。
    def create_scraping_result_injection_prompt_inputs(
        self,
        ai_input_id: int,
        ai_input_field_id: int,
        user_input: str,
        result_injection: str,
        prompt: str,
    ) -> List[PromptInput]:
        prompt_inputs: List[PromptInput] = []

        prompt_input: PromptInput = PromptInput(
            input=user_input,
            ai_input_id=ai_input_id,
            ai_input_field_id=ai_input_field_id,
            result_json={
                "input": user_input,
                "result_injection": result_injection,
                "prompt": prompt,
            },
        )
        prompt_inputs.append(prompt_input)

        return prompt_inputs
