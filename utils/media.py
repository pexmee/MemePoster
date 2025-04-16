import os
from contextlib import contextmanager
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import IO, Generator
from urllib.parse import urlparse

import pycurl


def download_from_url(url: str) -> bytes:
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.NOBODY, False)
    curl.perform()
    return buffer.getvalue()


@contextmanager
def temp_media_file(url: str) -> Generator[IO[bytes], None, None]:
    content = download_from_url(url)
    parsed_url = urlparse(url)
    image_suffix = os.path.splitext(parsed_url.path)[1]
    with NamedTemporaryFile(delete=True, suffix=image_suffix) as file:
        file.write(content)
        file.flush()
        yield file
