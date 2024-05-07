from dataclasses import dataclass
from ai_products.domains.ai.ai_request_data.ai_request_datas import AiRequestDatas


@dataclass
class AiRequestParams:
    task_id: int
    work_id: int
    ai_type_id: int
    request_data: AiRequestDatas
