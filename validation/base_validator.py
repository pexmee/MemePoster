import logging
from abc import ABC, abstractmethod

from memedata.memes import Meme
from utils.cache import CacheHandler

logger = logging.getLogger("pansophical_memes")


class BaseValidator(ABC):
    def __init__(self, cache: CacheHandler, platform_name: str):
        self.cache = cache
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})

    @abstractmethod
    def validate_meme(self, meme: Meme) -> bool:
        pass
