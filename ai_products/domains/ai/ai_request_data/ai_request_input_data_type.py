from typing import TypeAlias, Union

from ai_products.domains.ai.ai_request_data.scraping_prompt import ScrapingPrompt
from ai_products.domains.ai.ai_request_data.table_output_example import (
    TableOutputExample,
)


# BaseAiRequestInputDataに関するクラスをまとめて型定義
AiRequestInputDataType: TypeAlias = Union[ScrapingPrompt, TableOutputExample]
