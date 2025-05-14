from fastapi import APIRouter
from ariadne import QueryType, MutationType, SubscriptionType, make_executable_schema, gql
from ariadne.asgi import GraphQL
from graphql import GraphQLResolveInfo
from ariadne.types import GraphQLError
import mock_db.database as db
from typing import Any, Dict
from pydantic import ValidationError
from mock_db.resources import BookCreateRequest, BookUpdateRequest
from mock_db.error import ErrorMessage, SuccessMessage

router = APIRouter()

# Load your GraphQL schema
with open("schema.graphql") as f:
    type_defs = gql(f.read())

# Define types
query = QueryType()
mutation = MutationType()
subscription = SubscriptionType()


# Query resolvers
@query.field("books")
def resolve_books(_, info: GraphQLResolveInfo):
    return db.get_books()

@query.field("book")
def resolve_book(_, info: GraphQLResolveInfo, id):
    try:
        try:
            book_id = int(id)
        except ValueError:
            raise ErrorMessage(message="Book ID must be an integer", error_code=400)
        return db.get_book_by_id(book_id)
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to get book by id: {str(e)}", extensions={"status": 500})

@query.field("authors")
def resolve_authors(_, info: GraphQLResolveInfo):
    try:
        return db.get_authors()
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to get authors: {str(e)}", extensions={"status": 500})

@query.field("author")
def resolve_author(_, info: GraphQLResolveInfo, id):
    try:
        return db.get_author_by_id(int(id))
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to get author by id: {str(e)}", extensions={"status": 500})


# Mutation resolvers
@mutation.field("createBook")
def resolve_create_book(_, info: GraphQLResolveInfo, title, release_year, author_id):
    try:
        return db.create_book(
            book_create_request=BookCreateRequest(
                title=title,
                release_year=int(release_year),
                author_id=int(author_id)
            )
        )
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to create a book: {str(e)}", extensions={"status": 500})


@mutation.field("updateBook")
def resolve_update_book(_, info: GraphQLResolveInfo, id, title=None, release_year=None, author_id=None):
    try:
        if author_id is not None:
            try:
                author_id = int(author_id)
            except ValueError:
                raise ErrorMessage(message="Author ID must be an integer", error_code=400)
    
        return db.update_book(
            book_id=int(id),
            book_update_request=BookUpdateRequest(
                title=title,
                release_year=int(release_year) if release_year is not None else None,
                author_id=int(author_id) if author_id is not None else None
            )
        )
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to update a book: {str(e)}", extensions={"status": 500})

@mutation.field("deleteBook")
def resolve_delete_book(_, info: GraphQLResolveInfo, id):
    try:
        try:
            book_id = int(id)
        except ValueError:
            raise ErrorMessage(message="Book ID must be an integer", error_code=400)
        return db.delete_book(int(book_id))
    except ErrorMessage as e:
        raise GraphQLError(message=e.message, extensions={"status": e.error_code})
    except Exception as e:
        raise GraphQLError(message=f"Internal Server Error while trying to delete a book: {str(e)}", extensions={"status": 500})


# Build executable schema
schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    subscription,
)

# Create a GraphQL app and mount it
graphql_app = GraphQL(schema, debug=True)

router.add_route("/graphql", graphql_app)
router.add_websocket_route("/graphql", graphql_app)