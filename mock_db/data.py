from .entities import BookEntity, AuthorEntity
from typing import Literal

_book_id: int = 3
_author_id: int = 3

# Mock data
books = [
    BookEntity(id=1, title="Book Title A", release_year=2001, author_id=1),
    BookEntity(id=2, title="Book Title B", release_year=2002, author_id=2),
    BookEntity(id=3, title="Book Title C", release_year=2003, author_id=3),
]

authors = [
    AuthorEntity(id=1, name="Author A"),
    AuthorEntity(id=2, name="Author B"),
    AuthorEntity(id=3, name="Author C"),
]

def increment_id(entity_type: Literal["book", "author"]) -> int:
    """Increment the ID for a given entity type."""
    global _book_id, _author_id
    if entity_type == "book":
        _book_id += 1
        return _book_id
    elif entity_type == "author":
        _author_id += 1
        return _author_id
    else:
        raise ValueError("Invalid entity type. Use 'book' or 'author'.")