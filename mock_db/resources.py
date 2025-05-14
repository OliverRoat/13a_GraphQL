from pydantic import BaseModel, ConfigDict

class BookAuthorResource(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class BookResource(BaseModel):
    id: int
    title: str
    release_year: int
    author_id: int
    author: BookAuthorResource

    model_config = ConfigDict(from_attributes=True)
    

class BookCreateRequest(BaseModel):
    title: str
    release_year: int
    author_id: int
    
class BookUpdateRequest(BaseModel):
    title: str | None = None
    release_year: int | None = None
    author_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

class AuthorBookResource(BaseModel):
    id: int
    title: str
    release_year: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorResource(BaseModel):
    id: int
    name: str
    books: list[AuthorBookResource]

    model_config = ConfigDict(from_attributes=True)
    
