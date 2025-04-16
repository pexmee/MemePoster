import logging
import os
from typing import IO

import tweepy  # type: ignore

from memedata.memes import Meme
from posting.poster import PlatformPoster

logger = logging.getLogger("pansophical_memes")


class XPoster(PlatformPoster):
    def __init__(self, platform_name: str):
        super().__init__(platform_name)
        self._consumer_key = os.getenv("TWITTER_API_KEY")
        self._consumer_secret = os.getenv("TWITTER_API_SECRET")
        self._access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self._access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self._bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    def _get_apiv1(self) -> tweepy.API:
        """Authenticates to X using APIv1 Oauth1UserHandler"""
        self.logger.debug("Authenticating for X APIv1 with OAuth1UserHandler.")
        auth = tweepy.OAuth1UserHandler(
            consumer_key=self._consumer_key,
            consumer_secret=self._consumer_secret,
            access_token=self._access_token,
            access_token_secret=self._access_token_secret,
        )
        return tweepy.API(auth, wait_on_rate_limit=True)

    def _get_apiv2(self) -> tweepy.Client:
        """Authenticates to X using APIv2 Client"""
        self.logger.debug("Authenticating for X APIv2 with Client.")
        return tweepy.Client(
            bearer_token=self._bearer_token,
            consumer_key=self._consumer_key,
            consumer_secret=self._consumer_secret,
            access_token=self._access_token,
            access_token_secret=self._access_token_secret,
            wait_on_rate_limit=True,
        )

    def post_meme(self, file: IO[bytes], meme: Meme) -> None:
        api = self._get_apiv1()
        client = self._get_apiv2()
        media = api.media_upload(file.name)
        text = f"Original title: '{meme.title.strip()}' Credit: {meme.credit}"
        self.logger.info(f"Tweeting: '{text}' with media: {meme.url}")
        client.create_tweet(text=text, media_ids=[media.media_id])
