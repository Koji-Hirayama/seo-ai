from typing import List
from pydantic import BaseModel
from ai_products.services.ai.scraping.unstructured_url_loader_service import (
    UnstructuredURLLoaderService,
)


class ScrapingResult(BaseModel):
    url: str
    result: str


class GetScrapingResultsService:
    def get_results(self, urls: List[str]) -> List[ScrapingResult]:
        url_loader_service = UnstructuredURLLoaderService()
        datas = url_loader_service.url_loader(urls)
        results: List[ScrapingResult] = []
        for data in datas:
            text = data.page_content
            # \r \n を削除
            text = text.replace("\r", "")
            text = text.replace("\n", "")
            # スペースを削除
            text = text.replace(" ", "")
            # URL取得
            url = data.metadata["source"]
            results.append(ScrapingResult(url=url, result=text))
        return results
