import os
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from newspaper import Article
from pydantic import BaseModel

load_dotenv()


class CrawlerBase(BaseModel, ABC):
    url: str
    depth: int = int(os.getenv("CRAWL_DEPTH", "1"))
    max_pages: int = 100
    max_time: int = 60

    def __call__(self) -> str:
        """
        Call `self.crawl` method.
        """
        return self.crawl()

    @abstractmethod
    def crawl(self, *args, **kwargs) -> str:
        """
        Crawl the passed URL and return content as string.
        """
        pass

    def request_url(self, url: str) -> str | None:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve the webpage.")
                return None
        except Exception as e:
            print(e)
            raise

    def request_article(self, url) -> str | None:
        article = Article(url)
        try:
            article.download()
            article.parse()
        except Exception as e:
            print(f"Error downloading or parsing article: {e}")
            return None
        return article.text

    def request_sitemap_urls(self, url: str) -> list[str] | None:
        html_content = self.request_url(url)
        soup = BeautifulSoup(html_content, features="xml")
        return [x.string for x in soup.find_all("url")]


class JinaCrawler(CrawlerBase):
    url_prefix: str = "https://r.jina.ai/"
    JINA_API_KEY: str = os.getenv("JINA_API_KEY")

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.JINA_API_KEY}",
        }

    def crawl(self) -> str:
        resp = requests.get(
            os.path.join(self.url_prefix, self.url), headers=self.headers
        )
        return resp.text


if __name__ == "__main__":
    crawl_website_url = "https://docs.imgproxy.net/"

    # Crawl single url via JinaCrawler
    crawl_jina = JinaCrawler(url=crawl_website_url)
    print(crawl_jina.crawl())

    # Crawl sitemap urls
    # sitemap = "https://www.xomnia.com/sitemap.xml"
    # urls: list[str] = request_sitemap_urls(sitemap)
    # for url in urls[:10]:
    #     crawl_website = CrawlWebsite(url=url)
    #     print(url)
    #     print("="*50)
    #     print(crawl_website.crawl())
    #     print("\n\n\n")
