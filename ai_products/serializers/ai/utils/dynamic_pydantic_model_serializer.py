from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, List, Type
from utils.errors import ErrorType, CustomApiErrorException, ErrorDetail


class AiOutputPydanticModelSerialiser:
    # Pydanticモデルを動的に生成する関数
    def create_base_model(self, data: Dict[str, Any]) -> Type[BaseModel]:
        try:
            namespace = {"__annotations__": {}}
            for item in data["keys"]:
                key = item["key"]
                description = item.get("description", "")
                type_string = item.get("type", "str")  # JSONから型情報を取得
                field_type = self._get_type_from_string(
                    type_string
                )  # 型名をPythonの型に変換
                # リスト指定の場合は、keyがList指定の場合は、examplesをList様に変換
                if type_string.startswith("List[") and type_string.endswith("]"):
                    examples: List[List[Any]] = [item.get("examples", [])]
                else:
                    examples: List[Any] = item.get("examples", [])

                namespace[key] = Field(
                    default=None, description=description, examples=examples
                )
                namespace["__annotations__"][key] = field_type

            DynamicModel = type("DynamicModel", (BaseModel,), namespace)

            # Tableクラスの定義と生成
            class Datas(BaseModel):
                datas: List[DynamicModel]

        except ValidationError as e:
            raise CustomApiErrorException(
                error_type=ErrorType.AI_OUTPUT_PYDANTIC_MODEL_BAD_REQUEST,
                message="正しくて定義されていません。",
            )

        return Datas

    # create_model作成時のモデルのフィールドのkeyの型を指定の型に変換
    def _get_type_from_string(self, type_string: str) -> Type[Any]:
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }

        if type_string.startswith("List[") and type_string.endswith("]"):
            # ジェネリック型の処理
            inner_type_str = type_string[5:-1]
            inner_type = self._get_type_from_string(inner_type_str)
            return List[inner_type]
        else:
            return type_mapping.get(type_string, str)
