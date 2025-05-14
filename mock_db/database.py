from .data import books, authors, increment_id
from .entities import BookEntity, AuthorEntity
from .resources import BookResource, BookCreateRequest, BookUpdateRequest, AuthorResource
from typing import List, Optional, Union
from .error import DatabaseError, SuccessMessage


def get_books(author: Optional[AuthorEntity] = None) -> List[BookResource]:
    """Retrieve all books with their authors resolved."""
    if author is not None and not isinstance(author, AuthorEntity):
        raise DatabaseError(f"Unable to get Books: Invalid author entity provided, must be either None or an AuthorEntity, not {type(author).__name__}.")
    book_resources = []
    for book in books:
        if author is not None and book.author_id != author.id:
            continue
        try:
            author_resource = author.as_resource(book_resources) if isinstance(author, AuthorEntity) else get_author_by_id(book.author_id)
        
            book_resource = book.as_resource(author_resource)
            book_resources.append(book_resource)
        except DatabaseError as e:
            raise DatabaseError(f"Unable to get Books: {e.message}.", e.error_code)
    return book_resources


def get_book_by_id(book_id: Union[int, str]) -> Optional[BookResource]:
    """Retrieve a book by its ID with its author resolved."""
    if not isinstance(book_id, int) or isinstance(book_id, bool):
        raise DatabaseError(f"Unable to get Book by ID, Book ID must be an INT, not: {type(book_id).__name__}.", 400)
    for book in books:
        if book.id == book_id:
            try:
                author = get_author_by_id(book.author_id)
                return book.as_resource(author)
            except DatabaseError as e:
                raise DatabaseError(f"Unable to get Book by ID: {e.message}.", e.error_code)
    raise DatabaseError(f"Unable to find book with ID {book_id}.", 404)

def create_book(book_create_request: BookCreateRequest) -> BookResource:
    """Create a new book and return it with its author resolved."""
    if not isinstance(book_create_request, BookCreateRequest):
        raise DatabaseError(f"Unable to create Book: Invalid request, must be a BookCreateRequest, not {type(book_create_request).__name__}.")
    book_id = increment_id("book")
    try:
        author = get_author_by_id(book_create_request.author_id)
        
    except DatabaseError as e:
        raise DatabaseError(f"Unable to create Book: {e.message}.", e.error_code)
    new_book = BookEntity(id=book_id, **book_create_request.model_dump())
    books.append(new_book)
    
    return new_book.as_resource(author)


def update_book(book_id: int, 
                book_update_request: BookUpdateRequest
) -> BookResource:
    """Update an existing book and return it with its author resolved."""
    if not isinstance(book_update_request, BookUpdateRequest):
        raise DatabaseError(f"Unable to update Book: Invalid request, must be a BookUpdateRequest, not {type(book_update_request).__name__}.")
    if not isinstance(book_id, int) or isinstance(book_id, bool):
        raise DatabaseError(f"Unable to update Book: Invalid book ID, must be an INT, not {type(book_id).__name__}.", 400)
    for book in books:
        if book.id == book_id:
            updated_book = book.model_copy()
            if book_update_request.title is not None:
                updated_book.title = book_update_request.title
            if book_update_request.release_year is not None:
                updated_book.release_year = book_update_request.release_year
            if book_update_request.author_id is not None:
                try:
                    author = get_author_by_id(book_update_request.author_id)
                except DatabaseError as e:
                    raise DatabaseError(f"Unable to update Book: {e.message}.", e.error_code)
                updated_book.author_id = book_update_request.author_id
            books.remove(book)
            books.append(updated_book)
            author = get_author_by_id(updated_book.author_id)
            return updated_book.as_resource(author)
    raise DatabaseError(f"Unable to update Book could not find a book with ID {book_id}.", 404)

def delete_book(book_id: int) -> SuccessMessage:
    """Delete a book by its ID."""
    if not isinstance(book_id, int) or isinstance(book_id, bool):
        raise DatabaseError(f"Unable to delete book: Invalid book ID given, must be an int, not {type(book_id).__name__}.", 400)
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return SuccessMessage(message="Book deleted successfully.")
    raise DatabaseError(f"Unable to delete book: Book with ID {book_id} not found.", 404)


def get_authors() -> List[AuthorResource]:
    """Retrieve all authors with their books resolved."""
    author_resources = []
    for author in authors:
        try:
            books_by_author = get_books(author)
        except DatabaseError as e:
            raise DatabaseError(f"Unable to get authors: {e.message}.", e.error_code)
        author_resources.append(author.as_resource(books_by_author))
    return author_resources


def get_author_by_id(author_id: int) -> AuthorResource:
    """Retrieve an author by their ID with their books resolved."""
    if not isinstance(author_id, int) or isinstance(author_id, bool):
        raise DatabaseError(f"Invalid author ID: {author_id}.", 400)
    for author in authors:
        if author.id == author_id:
            books_by_author = get_books(author)
            return author.as_resource(books_by_author)
    raise DatabaseError(f"Unable to find author with ID {author_id}.", 404)
