import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CRAWLER_NAME = os.getenv("CRAWLER")


# Cached dirs
SRC_DIR = Path(__file__).resolve().parent
CACHE_DIR = SRC_DIR.parent / "cache"
CACHE_DATA_DIR = CACHE_DIR / "data"
