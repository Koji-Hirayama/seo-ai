from typing import List
from langchain.schema import HumanMessage
from ai_products.services import UnstructuredURLLoaderService


class GetScrapingPromptMessage:

    def get_human_message(self, input: str, urls: List[str]) -> HumanMessage:
        scraping = UnstructuredURLLoaderService()
        scraping_datas = scraping.url_loader(urls)
        context = "["
        for data in scraping_datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            # コンテキストに連結
            if context != "[":
                context += ",\n\n"
            context += '"' + text + '"'
        context += "]"
        PROMPT_TEMPLETE = """次のコンテキストを元に、指示文への回答をしてください。\n
        ・指示文:\n{text}\n
        ・コンテキスト:\n{context}
        """
        return HumanMessage(content=PROMPT_TEMPLETE.format(context=context, text=input))
