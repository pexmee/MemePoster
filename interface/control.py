import logging

from fetching import Fetcher
from posting import Poster
from utils.cache import CacheHandler
from utils.waiting import Waiter

logger = logging.getLogger("pansophical_memes")
LOGGING_INTERVAL = 10


class RequestController:
    def __init__(
        self,
        cache: CacheHandler,
        fetcher: Fetcher,
        poster: Poster,
        waiter: Waiter,
        max_meme_amount: int,
        hours_between_posts: int,
        platform_name: str,
    ):
        self.cache = cache
        self.fetcher = fetcher
        self.poster = poster
        self.waiter = waiter
        self.max_meme_amount = max_meme_amount
        self.hours_between_posts = hours_between_posts
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})

    def run(self) -> None:
        try:
            self.fetcher.select_memes(self.max_meme_amount)
            for file, meme in self.fetcher.download_memes():
                self.waiter.wait_for_window()
                self.poster.post_meme(file, meme)
                self.cache.store_meme(meme)
                self.waiter.wait(self.hours_between_posts, LOGGING_INTERVAL)

        except Exception as exc:
            self.logger.error(
                f"Exception in Controller.run: {exc}",
                exc_info=exc,
                stack_info=True,
            )
            raise exc
