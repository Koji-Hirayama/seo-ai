from typing import Any, Dict, List, Type
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, RetryOutputParser
from langchain_community.callbacks import get_openai_callback
from langchain.schema import HumanMessage, SystemMessage, AIMessage, FunctionMessage
from langchain_community.document_loaders.url import UnstructuredURLLoader
import time
import json
from pydantic import BaseModel, Field


class Points(BaseModel):
    texts: list[str] = Field(
        description="訴求文",
        examples=[
            [
                "最短60分の迅速施術と肌への負担を軽減するSHR脱毛採用",
                "肌質・毛質に合わせた独自開発の脱毛器と高度な技術で、丁寧な脱毛を実現",
            ]
        ],
    )


class SimpleLlmService:
    def chat(self):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        # プロンプトのテンプレート文章を定義
        template = """
        次の文章に誤字がないか調べて。誤字があれば訂正してください。
        {sentences_before_check}
        """

        messages = [
            SystemMessage(content="あなたは優秀な校正者です。"),
            HumanMessage(
                content=template.format(
                    sentences_before_check="こんんんちわ、真純です。"
                )
            ),
        ]

        prompt_token_size = llm.get_num_tokens_from_messages(messages=messages)
        print(f"{prompt_token_size =}")
        # チェーンを実行し、結果を表示
        with get_openai_callback() as cb:
            output = llm.predict_messages(messages=messages)
            print(output)
            print(cb)
            print("===========")
            print(f"{cb.total_tokens =}")
            print(f"{cb.prompt_tokens =}")
            print(f"{cb.completion_tokens =}")
            print(f"{cb.successful_requests =}")
            print(f"{cb.total_cost =}")
        return output

    # url: str, question: str, output_example_table: Dict
    def chat_PydanticOutputParser(self):
        start_time = time.time()
        loader = UnstructuredURLLoader(
            urls=["https://stlassh.com/method/"],
            ssl_verify=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            },
        )
        datas = loader.load()
        context = ""
        for data in datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            context += text + "\n\n" + "=======================" + "\n\n"
        print(context)
        # 与えられた辞書
        data = {
            "keys": [
                # {"key": "title", "description": "タイトルに関する"},
                {"key": "content", "description": "強みを箇条書き", "type": List[str]},
            ]
        }
        mock_data = self.create_model(data)
        # OutputParserを用意する
        parser = PydanticOutputParser(pydantic_object=mock_data)
        # プロンプトを作成
        prompt = PromptTemplate.from_template(
            template="""{query}\n\n{format_instructions}\n""",
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        PROMPT_TEMPLETE = """以下のコンテキストから脱毛に関する強みを3パターン作成してください。
        {context}
        """

        print("=======================")
        # messages = [
        #     HumanMessage(content=prompt.to_string()),
        # ]

        # chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, n=1)
        chat = ChatOpenAI(model_name="gpt-3.5-turbo-1106")
        chain = prompt | chat | parser
        with get_openai_callback() as cb:
            # 応答を得る
            output = chain.invoke({"query", PROMPT_TEMPLETE.format(context=context)})
            print(output)
            print(cb)
            print("===========")
            print(f"{cb.total_tokens =}")
            print(f"{cb.prompt_tokens =}")
            print(f"{cb.completion_tokens =}")
            print(f"{cb.successful_requests =}")
            print(f"{cb.total_cost =}")

        return output

    def chat_function_calling(self):
        tart_time = time.time()
        loader = UnstructuredURLLoader(
            urls=["https://stlassh.com/method/"],
            ssl_verify=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            },
        )
        datas = loader.load()
        context = ""
        for data in datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            context += text + "\n\n" + "=======================" + "\n\n"
        print(context)
        # 与えられた辞書(配列指定パターン)
        # data = {
        #     "keys": [
        #         # {"key": "title", "description": "タイトルに関する"},
        #         {
        #             "key": "content",
        #             "description": "訴求文",
        #             "examples": [
        #                 [
        #                     "最短60分の迅速施術と肌への負担を軽減するSHR脱毛採用",
        #                     "肌質・毛質に合わせた独自開発の脱毛器と高度な技術で、丁寧な脱毛を実現",
        #                 ]
        #             ],
        #             "type": "List[str]",
        #         },
        #     ]
        # }
        # 与えられた辞書(配列指定パターン)
        data2 = {
            "keys": [
                # {"key": "title", "description": "タイトルに関する"},
                {
                    "key": "content",
                    "description": "訴求文",
                    "examples": ["最短60分の迅速施術と肌への負担を軽減するSHR脱毛採用"],
                    "type": "str",
                },
            ]
        }
        mock_data = self.create_model(data)
        output_points_function = {
            "name": "output_points",
            "description": "脱毛店舗の強みを作成する",
            "parameters": mock_data.model_json_schema(),
        }
        functions = [output_points_function]

        PROMPT_TEMPLETE = """以下のコンテキストから脱毛に関する強みを10パターン作成してください。
        {context}
        """
        messages = [HumanMessage(content=PROMPT_TEMPLETE.format(context=context))]
        chat = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0, n=1)
        first_response = chat.predict_messages(
            messages=messages,
            functions=functions,
            # function_call={"name": output_points_function["name"]},
        )

        try:
            function_name = first_response.additional_kwargs["function_call"]["name"]
            function_args = json.loads(
                first_response.additional_kwargs["function_call"]["arguments"]
            )
            first = mock_data.model_validate_json(
                first_response.additional_kwargs["function_call"]["arguments"]
            )
        except json.JSONDecodeError as e:
            # エラーが発生した場合、エラーメッセージと位置を表示
            print(f"JSON解析エラー: {e.msg}")
            print(f"エラー位置: 行 {e.lineno}, 列 {e.colno}")

        function_message = FunctionMessage(
            name=function_name, content=first.model_dump_json()
        )
        messages.append(function_message)
        return messages

    def test_ai(
        self, url: str, input: str, input_table: str, output_example_table: BaseModel
    ):
        # return {
        #     "url": url,
        #     "input": input,
        #     "output_example_table": output_example_table,
        # }
        tart_time = time.time()
        loader = UnstructuredURLLoader(
            urls=[url],
            ssl_verify=False,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            },
        )
        datas = loader.load()
        context = ""
        for data in datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            context += text + "\n\n" + "=======================" + "\n\n"
        print(context)
        mock_data = output_example_table

        output_points_function = {
            "name": "output_points",
            "description": input_table,  # "強み・特徴を作成する"
            "parameters": mock_data.model_json_schema(),
        }

        functions = [output_points_function]

        PROMPT_TEMPLETE = """次のコンテキストから{input}\n
        {context}
        """
        messages = [
            HumanMessage(content=PROMPT_TEMPLETE.format(context=context, input=input))
        ]
        chat = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0, n=1)
        first_response = chat.predict_messages(
            messages=messages,
            functions=functions,
            # function_call={"name": output_points_function["name"]},
        )

        try:
            function_name = first_response.additional_kwargs["function_call"]["name"]
            function_args = json.loads(
                first_response.additional_kwargs["function_call"]["arguments"]
            )
            first = mock_data.model_validate_json(
                first_response.additional_kwargs["function_call"]["arguments"]
            )
        except json.JSONDecodeError as e:
            # エラーが発生した場合、エラーメッセージと位置を表示
            print(f"JSON解析エラー: {e.msg}")
            print(f"エラー位置: 行 {e.lineno}, 列 {e.colno}")

        function_message = FunctionMessage(
            name=function_name, content=first.model_dump_json()
        )
        messages.append(function_message)
        return {"prompt": messages[0].content, "output": first.model_dump()}

    sample_data = {
        "keys": [
            {
                "key": "content",
                "description": "訴求文",
                "examples": [
                    [
                        "最短60分の迅速施術と肌への負担を軽減するSHR脱毛採用",
                        "肌質・毛質に合わせた独自開発の脱毛器と高度な技術で、丁寧な脱毛を実現",
                    ]
                ],
                "type": "List[str]",
            },
        ]
    }

    # Pydanticモデルを動的に生成する関数
    def create_model(self, data: Dict[str, Any]) -> Type[BaseModel]:
        namespace = {"__annotations__": {}}
        for item in data["keys"]:
            key = item["key"]
            description = item.get("description", "")
            examples = item.get("examples", [])
            type_string = item.get("type", "str")  # JSONから型情報を取得
            field_type = self.get_type_from_string(
                type_string
            )  # 型名をPythonの型に変換

            namespace[key] = Field(
                default=None, description=description, examples=examples
            )
            namespace["__annotations__"][key] = field_type

        DynamicModel = type("DynamicModel", (BaseModel,), namespace)

        # Tableクラスの定義と生成
        class Table(BaseModel):
            datas: List[DynamicModel]

        return Table

    def get_type_from_string(self, type_string: str) -> Type[Any]:
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
