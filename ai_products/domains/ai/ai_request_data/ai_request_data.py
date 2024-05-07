from typing import List, Optional
from pydantic import BaseModel
from ai_products.domains.ai.ai_request_data.ai_request_input_data_type import (
    AiRequestInputDataType,
)
from ai_products.domains.ai.ai_request_data.table_output_example import (
    TableOutputExample,
)


class AiRequestData(BaseModel):
    ai_model_id: int
    input_datas: List[AiRequestInputDataType]

    def get_input_data(self, ai_input_id: int) -> Optional[AiRequestInputDataType]:
        """
        指定されたai_input_idを持つBaseAiRequestInputDataインスタンスを返します。
        存在しない場合はNoneを返します。
        """
        for input_data in self.input_datas:
            if input_data.ai_input_id == ai_input_id:
                return input_data
        return None

    def get_table_output_example_input_data(self) -> Optional[TableOutputExample]:
        """
        table_output_exampleのinpu_dataを探して返す。(一番最初)
        存在しない場合はNoneを返します。
        """
        for input_data in self.input_datas:
            if input_data.ai_input_type_id == 2:
                return input_data
        return None
