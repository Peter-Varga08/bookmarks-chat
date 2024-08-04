import os
import re
import tempfile
import unicodedata
from abc import ABC, abstractmethod

import requests
from newspaper import Article
from bs4 import BeautifulSoup
from dotenv import load_dotenv
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


class SoupCrawler(CrawlerBase):
    js: bool = False

    def crawl(self) -> str:
        tmp_file_path, _ = self.process()
        return self._read_temp_file(tmp_file_path)

    def _process_recursive(self, url, depth, visited_urls):
        if depth == 0 or url in visited_urls:
            return ""

        visited_urls.add(url)

        content = self.request_article(url)
        return content

        # raw_html = request_url(url)
        # if not raw_html:
        #     return content
        #
        # soup = BeautifulSoup(raw_html, "html.parser")
        # links = [a["href"] for a in soup.find_all("a", href=True)]
        # for link in links:
        #     full_url = urljoin(url, link)
        #     Ensure we're staying on the same domain
        # if self.url in full_url:
        #     content += self._process_recursive(full_url, depth - 1, visited_urls)  # type: ignore

        return content

    def _create_temp_file(self, content) -> tuple[str, str]:
        """Create a temporary file from a slugified url, with .txt extension"""
        file_name = self.slugify(self.url) + ".txt"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(content)  # type: ignore
        return temp_file_path, file_name

    def process(self) -> tuple[str, str]:
        # Extract and combine content recursively
        visited_urls = set()
        extracted_content = self._process_recursive(self.url, self.depth, visited_urls)

        # Create a temporary file
        return self._create_temp_file(extracted_content)

    def _read_temp_file(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            file_content = f.read().decode()
        return file_content

    @staticmethod
    def slugify(text):
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8")
        )
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        text = re.sub(r"[-\s]+", "-", text)
        return text


if __name__ == "__main__":
    # crawl_website_url = "https://docs.imgproxy.net/"
    crawl_website_url = "https://docs.imgproxy.net/"

    # Crawl single url via SoupCrawler
    crawl_website = SoupCrawler(url=crawl_website_url)
    print(crawl_website.crawl())

    # Crawl single url via JinaCrawler
    # crawl_jina = JinaCrawler(url=crawl_website_url)
    # print(crawl_jina.crawl())

    # Crawl sitemap urls
    # sitemap = "https://www.xomnia.com/sitemap.xml"
    # urls: list[str] = request_sitemap_urls(sitemap)
    # for url in urls[:10]:
    #     crawl_website = CrawlWebsite(url=url)
    #     print(url)
    #     print("="*50)
    #     print(crawl_website.crawl())
    #     print("\n\n\n")
