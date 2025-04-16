import os
import random

import praw  # type: ignore

from fetching.fetcher import PlatformFetcher
from memedata.memes import Meme
from validation.base_validator import BaseValidator


class RedditFetcher(PlatformFetcher):
    def __init__(self, validator: BaseValidator, platform_name: str):
        super().__init__(validator, platform_name)

    _reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_APP_ID"),
        client_secret=os.getenv("REDDIT_SECRET"),
        user_agent="meme_checker by im_pansophical",
    )
    _subreddits = [
        "memes",
        "prequelmemes",
        "terriblefacebookmemes",
    ]

    def select_memes_impl(self, amount: int) -> None:
        self.memes = set()
        self.logger.info(f"Selecting {amount} memes")
        while len(self.memes) < amount:
            subreddit = random.choice(self._subreddits)
            submissions: list[praw.reddit.models.Submission] = [
                s
                for s in self._reddit.subreddit(subreddit).top(
                    time_filter="day", limit=amount
                )
            ]
            remaining = amount - len(self.memes)
            to_fetch = min(len(submissions), remaining if remaining > 0 else 0)
            if to_fetch == 0:
                break

            self.logger.info(f"Getting {to_fetch} memes from subreddit /r/{subreddit}")
            for submission in random.sample(submissions, k=to_fetch):
                if submission.over_18:
                    self.logger.debug(
                        f"{submission.title} by {submission.author.name} on /r/{subreddit} was marked as NSFW. Skipping.."
                    )
                    continue  # We don't want NSFW stuff.

                meme = Meme(
                    url=submission.url,
                    author=(submission.author.name if submission.author else "Unknown"),
                    title=submission.title,
                    credit=f"Posted on reddit.com/r/{subreddit} by {'/u/' + submission.author.name if submission.author.name != "Unknown" else submission.author.name}",
                )
                if not self.validator.validate_meme(meme):
                    self.logger.debug(f"{meme.url} did not pass validation, skipping")
                    continue

                self.memes.add(meme)

        self.logger.info(
            f"Selected {len(self.memes)} memes for {self.validator.cache.platform_name}"
        )
