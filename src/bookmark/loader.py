import json

from bookmark.config import BRAVE_BOOKMARKS_PATH
from bookmark.models import BookmarkCollection


def load_bookmarks() -> BookmarkCollection:
    with open(BRAVE_BOOKMARKS_PATH) as file:
        bookmarks = json.load(file)
    return BookmarkCollection(**bookmarks)
