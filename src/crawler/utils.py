import os

import polars as pl
from tqdm import tqdm

from bookmark.loader import load_bookmarks
from bookmark.models import Link
from bookmark.utils import get_valid_folders_dict
from config import CRAWLER_NAME, CACHE_DATA_DIR
from crawler import SoupCrawler, JinaCrawler


def crawl_contents_from_links(links: list[list[Link]]) -> None:
    for tab in tqdm(links):
        for link in tqdm(tab):
            if not get_valid_folders_dict()[link.folder.lower().split("/")[0]]:
                continue
            print(f"Processing link for folder [{link.folder}].")
            try:
                if CRAWLER_NAME == "SOUP":
                    crawl_website = SoupCrawler(url=link.url)
                elif CRAWLER_NAME == "JINA":
                    crawl_website = JinaCrawler(url=link.url)
                else:
                    raise OSError(
                        "Unknown crawler type. Make sure you have the correct crawler type "
                        "specified in the .env file"
                    )
                content: str = crawl_website.crawl()

                # Save document contents
                os.makedirs(CACHE_DATA_DIR, exist_ok=True)

                # Create dumpable df from content and link
                link.name = link.name.replace("/", "or")
                if len(link.name) > 100:
                    link.name = link.name[:97] + "..."
                df_ = {"content": content}
                df_.update(link.model_dump())
                df_content = pl.DataFrame(df_)

                filename = CACHE_DATA_DIR / f"{link.name}.json"
                df_content.write_json(filename)
                print(f"Saved file {filename}.")
            except Exception as e:
                print(f"Error {e} for link: {link}")


if __name__ == "__main__":
    brave_bookmarks = load_bookmarks()
    links = brave_bookmarks.urls_all
    crawl_contents_from_links(links)
