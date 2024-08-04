import warnings
from typing import List

import typer
from typer import Typer

from bookmark.loader import load_bookmarks
from bookmark.models import Link
from vectordb.index import init_store
from vectordb.utils import create_documents_from_links, search_text

warnings.filterwarnings("ignore")

app = Typer()
vectorstore = init_store()


@app.command()
def crawl_all():
    """Crawl all Brave bookmarks from local bookmarks file."""
    brave_bookmarks = load_bookmarks()
    links: List[List[Link]] = brave_bookmarks.urls_all
    documents = create_documents_from_links(links=links)
    vectorstore.add_documents(documents)
    print(f"Crawled and added {len(documents)} documents to vectorstore.")


@app.command()
def search(text: str = typer.Argument(..., help="Text to search with.")):
    """Search for the document closest to `text`."""
    return search_text(vectorstore=vectorstore, text=text)


if __name__ == "__main__":
    app()

# Uncomment if need bookmarks by main folder
# ------------------------------------------
# urls = {}
# for bookmark in brave_bookmarks:
#     if bookmark.type == 'folder':
#         urls[bookmark.name] = bookmark.urls
#     else:
#         urls[bookmark.name] = bookmark.url

# pp(brave_bookmarks.urls_all)
