from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    id: int
    title: str
    author: str
    publication_date: date
    isbn: str
    page_count: int
    language: str
    genre: str
    description: str
    publisher: str
    availability: str
