from ai_products.domains.ai.ai_request_data.ai_request_data import AiRequestData
from ai_products.models import AiRequest, Work, User, Task
from typing import List


class CreateAiRequestService:

    def create_ai_request(
        self,
        task: Task,
        work: Work,
        user: User,
        request_data: List[AiRequestData],
        status: int,
    ):
        ai_request = AiRequest(
            task=task,
            work=work,
            user=user,
            request_data=request_data,
            status=status,
        )
        ai_request.save()
        return ai_request
