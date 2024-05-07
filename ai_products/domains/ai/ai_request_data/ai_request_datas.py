from typing import List
from pydantic import BaseModel
from ai_products.domains.ai.ai_request_data.ai_request_data import AiRequestData


class AiRequestDatas(BaseModel):
    ai_request_datas: List[AiRequestData]
