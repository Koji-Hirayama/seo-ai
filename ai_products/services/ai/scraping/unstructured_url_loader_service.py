from langchain_community.document_loaders.url import UnstructuredURLLoader
from typing import List


class UnstructuredURLLoaderService:
    def url_loader(self, urls: List[str]):
        loader = UnstructuredURLLoader(
            urls=urls,
            ssl_verify=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
            },
        )
        datas = loader.load()
        return datas
