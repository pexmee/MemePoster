from memedata.memes import Meme
from validation.base_validator import BaseValidator


class XValidator(BaseValidator):
    def validate_meme(self, meme: Meme):
        return not self.cache.meme_posted(meme)
