from dataclasses import dataclass


@dataclass(frozen=True)
class Meme:
    url: str
    author: str
    title: str
    credit: str

    def __hash__(self) -> int:
        return hash((self.url, self.author))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Meme):
            return NotImplemented

        return self.url == other.url and self.author == other.author
