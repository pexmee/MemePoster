import logging
import os
from typing import IO

from instagrapi import Client  # type: ignore
from instagrapi.exceptions import (FeedbackRequired,  # type: ignore
                                   LoginRequired)
from PIL import Image

from memedata.memes import Meme
from posting.poster import PlatformPoster

logger = logging.getLogger("pansophical_memes")


def handle_exception(client: Client, e):
    if isinstance(e, FeedbackRequired):
        message = client.last_json["feedback_message"]
        if "We restrict certain activity to protect our community" in message:
            client.logger.error(
                f"message from ig: {message}", exc_info=e, stack_info=True
            )
            # TODO: If this happens we probably want to wait X amount of days before we post again.
            # TODO: Perhaps we can add a blocker handle to each post call that just freezes for 3-4 days.
    else:
        client.logger.exception(e)
        raise e


class InstagramPoster(PlatformPoster):
    def __init__(self, platform_name: str):
        super().__init__(platform_name)
        self._client = Client(logger=self.logger, delay_range=[1, 3])
        self._client.handle_exception = handle_exception
        self._username = os.getenv("IG_USER")
        self._password = os.getenv("IG_PASSWORD")
        self._hashtags = [
            "#memes",
            "#meme",
            "#redditmemes",
            "#redditmeme",
            "#reddit",
            "#funny",
        ]

    def _auth(self) -> bool:
        self.logger.debug("Authenticating")
        session = (
            self._client.load_settings("instagram.json")
            if os.path.exists("instagram.json")
            else None
        )
        login = False
        if session:
            try:
                self._client.set_settings(session)
                login = self._client.login(self._username, self._password)
                try:
                    self._client.get_timeline_feed()
                except LoginRequired:
                    self.logger.info(
                        "Session is invalid, need to login via username and password"
                    )
                    old_session = self._client.get_settings()
                    self._client.set_settings({})
                    self._client.set_uuids(old_session["uuids"])
                    self._client.login(self._username, self._password)

            except Exception as exc:
                self.logger.error(
                    f"Exception in _auth",
                    exc_info=exc,
                    stack_info=True,
                )
        else:
            try:
                login = self._client.login(self._username, self._password)
            except Exception as exc:
                self.logger.error(
                    f"Couldn't login user using username and password",
                    exc_info=exc,
                    stack_info=True,
                )

        self._client.dump_settings("instagram.json")
        return login

    def _convert_to_jpeg(self, file: IO[bytes]) -> None:
        self.logger.debug(f"Filename: {file.name} is not jpeg, converting..")
        with Image.open(file.name) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(file.name, "jpeg")
            self.logger.debug(f"Converted {file.name} to jpeg")

    def post_meme(self, file: IO[bytes], meme: Meme) -> None:
        login = self._auth()
        self.logger.debug(f"logged in: {login}")
        if not file.name.endswith("jpeg"):
            self._convert_to_jpeg(file)

        caption = f"Original title: '{meme.title.strip()}', Credit: {meme.credit} {' '.join(self._hashtags)}"
        self.logger.info(f"Posting '{caption}' with media: {meme.url}")
        self._client.photo_upload(
            path=file.name,
            caption=caption,
        )
