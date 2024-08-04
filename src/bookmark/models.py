from functools import cached_property
from pathlib import Path
from typing import List, Dict, Optional, Any, Iterator

from pydantic import BaseModel


class Link(BaseModel):
    name: str
    url: str
    folder: str

    @property
    def path(self) -> str:
        return str(Path(self.folder) / self.name)


class BookmarkBase(BaseModel):
    date_added: str
    date_last_used: str
    date_modified: Optional[str] = None
    guid: str
    id: str
    name: str
    type: str


class Bookmark(BookmarkBase):
    meta_info: Optional[Dict[str, str]] = None
    url: Optional[str] = None  # used by URL types only, i.e. not by folders


class RootDetail(Bookmark):
    children: Optional[List["RootDetail"]] = None

    def __getitem__(self, item) -> Optional[List["RootDetail"]]:
        return self.children[item]

    def _get_urls_recursively(
        self, _urls: List[Link] = None, _path: Path = None, _depth: int = 1
    ) -> List[Link]:
        if _urls is None:
            _urls = []
            _path = Path(self.name)

        # if it's a folder type, go through all children
        if self.type == "folder":
            _path_len = len(_path.parts)
            if _depth > _path_len:
                _path = _path / self.name
            elif _path_len > _depth:
                _path = _path.parent

            for child in self.children:
                # if it's a URL type, add them to dict
                if child.type == "url":
                    _urls.append(
                        Link(name=child.name, url=child.url, folder=str(_path))
                    )
                else:
                    child._get_urls_recursively(_urls, _path, _depth + 1)
        else:
            # if it's a URL type, add them to dict
            _urls.append(Link(name=self.name, url=self.url, folder=""))
        return _urls

    @cached_property
    def urls(self, _urls: Dict[str, Any] = None) -> List[Link]:
        return self._get_urls_recursively()


class Roots(BaseModel):
    bookmark_bar: RootDetail
    other: RootDetail
    synced: RootDetail


class BookmarkCollection(BaseModel):
    checksum: str
    roots: Roots
    version: int

    def __getitem__(self, item: int) -> RootDetail:
        return self.bookmarks[item]

    def __iter__(self) -> Iterator[RootDetail]:
        return iter(self.bookmarks)

    @property
    def bookmarks(self) -> List[RootDetail]:
        return self.roots.bookmark_bar.children

    @cached_property
    def folders(self) -> List[str]:
        """Return name of all folders, whether empty or not."""
        return [x.name for x in self.bookmarks if x.type == "folder"]

    @cached_property
    def urls_top(self) -> Dict[str, str]:
        """Return all the urls that are not contained within a folder."""
        return {x.name: x.url for x in self.bookmarks if x.type == "url"}

    @cached_property
    def urls_all(self) -> List[List[Link]]:
        """Return all urls with name, link and folder, recursively."""
        return [x.urls for x in self.bookmarks]


RootDetail.update_forward_refs()
