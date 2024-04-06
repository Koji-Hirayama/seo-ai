from pydantic import BaseModel, Field
from typing import Any, Dict, List, Type


class AiOutputPydanticModelSerialiser:
    # Pydanticモデルを動的に生成する関数
    def create_model(self, data: Dict[str, Any]) -> Type[BaseModel]:
        namespace = {"__annotations__": {}}
        for item in data["keys"]:
            key = item["key"]
            description = item.get("description", "")
            examples = item.get("examples", [])
            type_string = item.get("type", "str")  # JSONから型情報を取得
            field_type = self._get_type_from_string(
                type_string
            )  # 型名をPythonの型に変換

            namespace[key] = Field(
                default=None, description=description, examples=examples
            )
            namespace["__annotations__"][key] = field_type

        DynamicModel = type("DynamicModel", (BaseModel,), namespace)

        # Tableクラスの定義と生成
        class Datas(BaseModel):
            datas: List[DynamicModel]

        return Datas

    # create_model作成時のモデルのフィールドのkeyの型を指定の型に変換
    def _get_type_from_string(self, type_string: str) -> Type[Any]:
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": List,
        }

        if type_string.startswith("List[") and type_string.endswith("]"):
            # ジェネリック型の処理
            inner_type_str = type_string[5:-1]
            inner_type = self.get_type_from_string(inner_type_str)
            return List[inner_type]
        else:
            return type_mapping.get(type_string, str)
