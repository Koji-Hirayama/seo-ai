from typing import List

from ai_products.services import UnstructuredURLLoaderService


class GetScrapingResultsService:
    def get_results(self, urls: List[str]):
        url_loader_service = UnstructuredURLLoaderService()
        datas = url_loader_service.url_loader(urls)
        results = []
        for data in datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            # URL取得
            url = data.metadata["source"]
            results.append({"url": url, "result": text})
        return results
