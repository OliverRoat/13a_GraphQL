from pydantic import BaseModel, ConfigDict
from .resources import BookAuthorResource, BookResource, AuthorBookResource, AuthorResource

class BookEntity(BaseModel):
    id: int
    title: str
    release_year: int
    author_id: int
    
    def as_resource(self, author: AuthorResource) -> BookResource:
        """Convert the entity to a resource."""
        # Create a BookAuthorResource instance
        book_author = BookAuthorResource(
            id=author.id, 
            name=author.name
            )
        
        return BookResource(
            id=self.id, 
            title=self.title, 
            release_year=self.release_year,
            author_id=self.author_id,
            author=book_author
            )

    model_config = ConfigDict(from_attributes=True)

class AuthorEntity(BaseModel):
    id: int
    name: str
    
    def as_resource(self, books: list[BookResource]) -> AuthorResource:
        """Convert the entity to a resource."""
        # Create a list of AuthorBookResource instances
        author_books = [
            AuthorBookResource(
                id=book.id, 
                title=book.title, 
                release_year=book.release_year,
                author_id=self.id
                ) for book in books
            ]
        
        return AuthorResource(
            id=self.id, 
            name=self.name,
            books=author_books
            )

    model_config = ConfigDict(from_attributes=True)
    



    
