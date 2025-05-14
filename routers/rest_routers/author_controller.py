from typing import List
from fastapi import APIRouter, Path, HTTPException
from mock_db.resources import AuthorResource
from mock_db.error import ErrorMessage
import mock_db.database as db
from pydantic import BaseModel

class AuthorListResponseResource(BaseModel):
    data: List[AuthorResource]

class AuthorResponseResource(BaseModel):
    data: AuthorResource



router = APIRouter()


@router.get(
    path="/authors",
    response_model=AuthorListResponseResource
)
def get_authors():
    try:
        author_resources = db.get_authors()
        return AuthorListResponseResource(data=author_resources)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to get authors: {str(e)}")
        


@router.get(
    path="/authors/{author_id}",
    response_model=AuthorResponseResource
)
def get_author(
    author_id: int = Path(...)
):
    try:
        author_resource = db.get_author_by_id(author_id)
        return AuthorResponseResource(data=author_resource)
    except ErrorMessage as e:
        raise HTTPException(status_code=e.error_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error while trying to get author by id: {str(e)}")