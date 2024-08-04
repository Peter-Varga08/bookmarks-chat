import pandas as pd
from langchain_core.documents import Document
from tqdm import tqdm

from crawler import SoupCrawler
from models import Link


def search_text(vectorstore, text: str) -> pd.DataFrame:
    query_docs = vectorstore.similarity_search_with_score(text, k=3)
    results_table = pd.DataFrame(
        {
            "Name": [d[0].metadata["name"] for d in query_docs],
            "URL": [d[0].metadata["url"] for d in query_docs],
            "Annotation": [d[0].page_content for d in query_docs],
            "Similarity": [1 - d[1] for d in query_docs],
        }
    )
    print(results_table)
    return results_table


def create_document(content: str, name: str, url: str, folder: str) -> Document:
    """Convert a parsed website content and link data into a `Document` object."""
    return Document(
        page_content=content, metadata={"name": name, "url": url, "folder": folder}
    )


def create_documents_from_links(links: list[list[Link]]) -> list[Document]:
    documents = []
    for tab in tqdm(links):
        for link in tqdm(tab):
            try:
                crawl_website = SoupCrawler(url=link.url)
                content: str = crawl_website.crawl()
                document = create_document(
                    content=content, name=link.name, url=link.url, folder=link.folder
                )
                documents.append(document)
            except Exception:
                print(f"Error for link: {link}")
    return documents
