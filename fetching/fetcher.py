import logging
from abc import ABC, abstractmethod
from threading import Lock
from typing import IO, Generator, Protocol

from memedata.memes import Meme
from utils.media import temp_media_file
from utils.sync import synchronized
from validation.base_validator import BaseValidator

logger = logging.getLogger("pansophical_memes")
_lock = Lock()


class Fetcher(Protocol):
    def select_memes(self, amount: int) -> None: ...
    def download_memes(self) -> Generator[tuple[IO[bytes], Meme], None, None]: ...


class PlatformFetcher(ABC):
    def __init__(self, validator: BaseValidator, platform_name: str) -> None:
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})
        self.memes: set[Meme] = (
            set()
        )  # To make sure each class instance has its own set
        self.validator = validator

    @synchronized(_lock)
    def select_memes(self, amount: int) -> None:
        self.select_memes_impl(amount)

    @abstractmethod
    def select_memes_impl(self, amount: int) -> None:
        pass

    def download_memes(self) -> Generator[tuple[IO[bytes], Meme], None, None]:
        for meme in self.memes:
            with temp_media_file(meme.url) as file:
                yield file, meme
