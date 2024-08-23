from dataclasses import dataclass

from api.dto.internal import Book


@dataclass
class AddBook(Book):
    pass
