from pathlib import Path

# BRAVE BROWSER FILE PATHS
BRAVE_PATH = Path(
    "~/.config/BraveSoftware/Brave-Browser/Default/"
).expanduser()  # expanduser converts '~' correctly
BRAVE_BOOKMARKS_PATH = BRAVE_PATH / "Bookmarks"
