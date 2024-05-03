from ai_products.models import PromptInput
from django.db.models.query import QuerySet


class GetPromptInputService:
    def get_prompt_inputs_by_prompt_id(self, prompt_id) -> QuerySet[PromptInput]:
        prompt_inputs = PromptInput.objects.filter(prompt_id=prompt_id)
        return prompt_inputs
