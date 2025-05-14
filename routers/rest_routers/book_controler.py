from typing import List
from fastapi import APIRouter, Path, Body, status, HTTPException
from mock_db.resources import BookResource, BookCreateRequest, BookUpdateRequest
import mock_db.database as db
from mock_db.error import ErrorMessage, SuccessMessage
from pydantic import BaseModel


class BookListResponseResource(BaseModel):
    data: List[BookResource]

class BookResponseResource(BaseModel):
    data: BookResource

class SuccessMessageResponseResource(BaseModel):
    data: SuccessMessage

router = APIRouter()

@router.get(
    path="/books",
    response_model=BookListResponseResource
)
def get_books():
    try:
        book_resources = db.get_books()
        return BookListResponseResource(data=book_resources)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to get books: {str(e)}")
        


@router.get(
    path="/books/{book_id}",
    response_model=BookResponseResource
)
def get_author(
    book_id: int = Path(...)
):
    try:
        book_resource = db.get_book_by_id(book_id)
        return BookResponseResource(data=book_resource)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while tying to get book by id: {str(e)}")


@router.post(
    path="/books",
    response_model=BookResponseResource
)
def create_book(
    book: BookCreateRequest
):
    try:
        book_resource = db.create_book(book)
        return BookResponseResource(data=book_resource)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as a:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to create a book: {str(e)}")


@router.put(
    path="/books/{book_id}",
    response_model=BookResponseResource
)
def update_book(
    book_id: int = Path(...),
    book: BookUpdateRequest = Body(...)
):
    try:
        book_resource = db.update_book(book_id, book)
        return BookResponseResource(data=book_resource)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to update a book: {str(e)}")



@router.delete(
    path="/books/{book_id}",
    response_model=SuccessMessageResponseResource
)
def delete_book(
    book_id: int = Path(...)
):
    try:
        success_message = db.delete_book(book_id)
        return SuccessMessageResponseResource(data=success_message)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to delete a book: {str(e)}")