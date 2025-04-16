import logging
import sqlite3
from threading import Lock

from memedata.memes import Meme

logger = logging.getLogger("pansophical_memes")


class SQLiteCache:
    def __init__(self, db_file: str = "cache.db") -> None:
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                platform_name TEXT NOT NULL,
                author TEXT NOT NULL,
                url TEXT NOT NULL,
                PRIMARY KEY (platform_name, author, url)
            );
            """
        )
        self.conn.commit()

    def add_entry(self, platform_name: str, author: str, url: str) -> None:
        """
        Adds a platform, author, and URL to the cache.
        If the combination already exists, this is a no-op.
        """
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO urls (platform_name, author, url)
            VALUES (?, ?, ?);
            """,
            (platform_name, author, url),
        )
        self.conn.commit()

    def url_exists(self, platform_name: str, author: str, url: str) -> bool:
        """
        Checks if a specific platform, author, and URL combination exists.
        """
        self.cursor.execute(
            """
            SELECT 1 FROM urls
            WHERE platform_name = ? AND author = ? AND url = ?;
            """,
            (platform_name, author, url),
        )
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()


class CacheHandler:
    write_lock = Lock()

    def __init__(
        self,
        cache: SQLiteCache,
        platform_name: str,
    ):
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})
        self.cache = cache
        self.platform_name = platform_name

    def meme_posted(self, meme: Meme) -> bool:
        exists = self.cache.url_exists(self.platform_name, meme.author, meme.url)
        self.logger.debug(f"author {meme.author} & url {meme.url} in cache: {exists}")
        return exists

    def store_meme(self, meme: Meme) -> None:
        with self.write_lock:
            self.logger.debug(f"Writing author {meme.author} & url {meme.url} to cache")
            self.cache.add_entry(self.platform_name, meme.author, meme.url)
