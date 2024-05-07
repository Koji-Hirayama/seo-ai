from pydantic import BaseModel


class BaseAiRequestInputData(BaseModel):
    ai_input_id: int
    ai_input_type_id: int
