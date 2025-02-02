import warnings
from typing import List

import typer
from typer import Typer

from bookmark.loader import load_bookmarks
from bookmark.models import Link
from crawler.utils import crawl_contents_from_links
from vectordb.index import init_store
from vectordb.utils import search_text, read_documents_from_cache

warnings.filterwarnings("ignore")

app = Typer()
vectorstore = init_store()


@app.command()
def crawl_documents() -> None:
    """Crawl all Brave bookmarks from local bookmarks files and upload them."""
    brave_bookmarks = load_bookmarks()
    links: List[List[Link]] = brave_bookmarks.urls_all
    crawl_contents_from_links(links)


@app.command()
def add_cached_documents() -> None:
    """Upload the cached documents to the vectorstore."""
    # Read documents from cache
    documents = read_documents_from_cache()
    vectorstore.add_documents(documents)
    print(f"Added {len(documents)} documents to vectorstore.")


@app.command()
def search(text: str = typer.Argument(..., help="Text to search with.")):
    """Search for the document closest to `text`."""
    return search_text(vectorstore=vectorstore, text=text)


if __name__ == "__main__":
    crawl_documents()

# Uncomment if need bookmarks by main folder
# ------------------------------------------
# urls = {}
# for bookmark in brave_bookmarks:
#     if bookmark.type == 'folder':
#         urls[bookmark.name] = bookmark.urls
#     else:
#         urls[bookmark.name] = bookmark.url

# pp(brave_bookmarks.urls_all)
