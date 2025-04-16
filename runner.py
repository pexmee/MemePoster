from interface.control import RequestController
from scheduling.schedule import Scheduler
from utils.cache import CacheHandler, SQLiteCache
from utils.config import Config


def main() -> None:
    cache = SQLiteCache()
    controllers: list[RequestController] = []
    for config in Config.from_json("config.json"):
        cache_handler = CacheHandler(cache, config.platform_name)
        validator = config.validator(cache_handler, config.platform_name)
        fetcher = config.fetcher(validator, config.platform_name)
        controller = RequestController(
            cache=cache_handler,
            fetcher=fetcher,
            poster=config.poster(config.platform_name),
            waiter=config.waiter(config.platform_name),
            max_meme_amount=config.max_meme_amount,
            hours_between_posts=config.hours_between_posts,
            platform_name=config.platform_name,
        )
        controllers.append(controller)

    scheduler = Scheduler(controllers)
    scheduler.start()


if __name__ == "__main__":
    main()
