import logging

from PIL import Image

from memedata.memes import Meme
from utils.media import temp_media_file
from validation.base_validator import BaseValidator

logger = logging.getLogger("pansophical_memes")


class InstagramValidator(BaseValidator):
    def _image_validation(self, meme: Meme) -> bool:
        # Yes, for instagram we kinda download it twice, but that's fine.
        # This will make everything much smoother.
        with temp_media_file(meme.url) as file:
            with Image.open(file.name) as img:
                width, height = img.size
                aspect_ratio = width / height
                if width > 1080 or (320 <= width <= 1080):
                    if 4 / 5 <= aspect_ratio <= 1.91:
                        self.logger.debug(
                            f"Image {meme.url} is supported with width {width} and aspect ratio {aspect_ratio}"
                        )

                        return True

            self.logger.debug(
                f"Image {meme.url} is not supported due to a width of {width} and an aspect ratio of {aspect_ratio}"
            )
            return False

    def validate_meme(self, meme: Meme) -> bool:
        if not any(
            [meme.url.endswith(x) for x in [".jpg", ".png", ".jpeg"]]
        ) or self.cache.meme_posted(meme):
            return False

        return self._image_validation(meme)
