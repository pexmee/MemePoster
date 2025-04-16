import logging
from abc import ABC, abstractmethod
from typing import IO, Protocol

from memedata.memes import Meme

logger = logging.getLogger("pansophical_memes")


class Poster(Protocol):
    def post_meme(self, file: IO[bytes], meme: Meme) -> None: ...


class PlatformPoster(ABC):
    def __init__(self, platform_name: str):
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})

    @abstractmethod
    def post_meme(self, file: IO[bytes], meme: Meme) -> None:
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__
