from typing import List
from ai_products.models import AiInputField
from ai_products.services.ai.scraping.get_scraping_results_service import (
    ScrapingResult,
)


class GetScrapingPromptMessageService:
    def __init__(self, context_input_field: AiInputField, input: str):
        self._context_input_field = context_input_field
        self._input = input

    def join_scraping_results_as_text(
        self, scraping_results: List[ScrapingResult]
    ) -> str:
        """
        ScrapingResultのリストからテキストを抽出し、一定のフォーマットで連結する。
        """
        result_context = "["
        for scraping_result in scraping_results:
            text = scraping_result.result
            if result_context != "[":
                result_context += ",\n\n"
            result_context += '"' + text + '"'
        result_context += "]"
        return result_context

    def get_scraping_result_injection_message(
        self, scraping_results: List[ScrapingResult]
    ) -> str:
        # コンテキストに連結
        scraping_result_context = self.join_scraping_results_as_text(scraping_results)
        context = self._context_input_field.context
        replaced_context = context.replace("{{input}}", self._input).replace(
            "{{result_injection}}", scraping_result_context
        )
        return replaced_context
