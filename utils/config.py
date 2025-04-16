import json
from dataclasses import dataclass
from typing import Generator

from fetching import Fetcher, PlatformFetcher, RedditFetcher
from posting.instagram import InstagramPoster
from posting.poster import PlatformPoster
from posting.x import XPoster
from utils.waiting import PlatformWaiter, WindowWaiter
from validation.base_validator import BaseValidator
from validation.instagram import InstagramValidator
from validation.x import XValidator

WAITER_MAP: dict[str, type[PlatformWaiter]] = {
    "instagram": WindowWaiter,
    "x": PlatformWaiter,
}

POSTER_MAP: dict[str, type[PlatformPoster]] = {
    "instagram": InstagramPoster,
    "x": XPoster,
}

FETCHER_MAP: dict[str, type[PlatformFetcher]] = {
    "instagram": RedditFetcher,
    "x": RedditFetcher,
}

VALIDATOR_MAP: dict[str, type[BaseValidator]] = {
    "instagram": InstagramValidator,
    "x": XValidator,
}


@dataclass(frozen=True)
class Config:
    platform_name: str
    post_during_day: bool
    poster: type[PlatformPoster]
    fetcher: type[PlatformFetcher]
    validator: type[BaseValidator]
    waiter: type[PlatformWaiter]
    max_meme_amount: int
    hours_between_posts: int

    @staticmethod
    def from_json(filename: str) -> Generator["Config", None, None]:
        with open(filename, "r") as read_h:
            data = json.load(read_h)
            for name, config in data.items():
                hours_between_posts = config["hours_between_posts"]
                post_during_day = config["post_during_day"]
                assert isinstance(hours_between_posts, int)
                assert isinstance(post_during_day, bool)
                max_meme_amount = (
                    (24 // hours_between_posts)
                    if not post_during_day
                    else (12 // hours_between_posts)
                )
                hours_between_posts = (
                    hours_between_posts * 60 * 60
                )  # Convert to hours in seconds
                yield Config(
                    platform_name=name,
                    hours_between_posts=hours_between_posts,
                    max_meme_amount=max_meme_amount,
                    post_during_day=post_during_day,
                    poster=POSTER_MAP[name],
                    fetcher=FETCHER_MAP[name],
                    validator=VALIDATOR_MAP[name],
                    waiter=WAITER_MAP[name],
                )
