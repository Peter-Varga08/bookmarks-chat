import os

import pandas as pd
import polars as pl
from langchain_core.documents import Document
from tqdm import tqdm

from bookmark.models import Link
from bookmark.utils import get_valid_folders_dict
from config import CRAWLER_NAME, CACHE_DATA_DIR
from crawler import SoupCrawler, JinaCrawler
from crawler.enums import CrawlerEnum


def _search_text(vectorstore, text: str, k: int = 3) -> pl.DataFrame:
    query_docs = vectorstore.similarity_search_with_score(text, k=k)
    return pl.DataFrame(
        {
            "Name": [d[0].metadata["name"] for d in query_docs],
            "URL": [d[0].metadata["url"] for d in query_docs],
            "Annotation": [d[0].page_content for d in query_docs],
            "Similarity": [1 - d[1] for d in query_docs],
        }
    )


def search_text(vectorstore, text: str) -> pl.DataFrame:
    matching_docs = _search_text(vectorstore, text)
    print(matching_docs)
    return matching_docs


def search_text_with_threshold(vectorstore, text: str) -> pl.DataFrame:
    matching_docs: pl.DataFrame = _search_text(vectorstore, text)
    return matching_docs.filter(pl.col("Similarity") >= 0.75)


def create_document(content: str, name: str, url: str, folder: str) -> Document:
    """Convert a parsed website content and link data into a `Document` object."""
    return Document(
        page_content=content, metadata={"name": name, "url": url, "folder": folder}
    )


def create_documents_from_links(links: list[list[Link]]) -> list[Document]:
    documents = []

    for tab in tqdm(links):
        docs_in_tab = []
        for link in tqdm(tab):
            if not get_valid_folders_dict()[link.folder.lower().split("/")[0]]:
                continue
            print(f"Processing link for folder [{link.folder}].")
            try:
                if CRAWLER_NAME == CrawlerEnum.SOUP:
                    crawl_website = SoupCrawler(url=link.url)
                elif CRAWLER_NAME == CrawlerEnum.JINA:
                    crawl_website = JinaCrawler(url=link.url)
                else:
                    raise OSError(
                        "Unknown crawler type. Make sure you have the correct crawler type "
                        "specified in the .env file"
                    )
                content: str = crawl_website.crawl()

                document = create_document(
                    content=content, name=link.name, url=link.url, folder=link.folder
                )
                docs_in_tab.append(document)
            except Exception as e:
                print(f"Error {e} for link: {link}")

        print(f"Number of documents created from tab: [{len(docs_in_tab)}].")
        documents.extend(docs_in_tab)

    print(f"Number of documents created from all links: [{len(documents)}].")
    return documents


# TODO: Throw error if CACHE_DATA_DIR does not exist or is empty
def read_documents_from_cache() -> list[Document]:
    """Read documents from cache."""
    documents = []
    for file in os.listdir(CACHE_DATA_DIR):
        if file.endswith(".json"):
            df = pd.read_json(CACHE_DATA_DIR / file)
            documents.append(
                create_document(
                    content=df["content"],
                    name=df["name"],
                    url=df["url"],
                    folder=df["folder"],
                )
            )
    return documents
