from fastapi import FastAPI
from routers.rest_routers.author_controller import router as author_router
from routers.rest_routers.book_controler import router as book_router
from routers.graphql_router.graphql_controller import router as graphql_router

# Initialize the FastAPI application
app = FastAPI()

app.include_router(author_router, prefix="/api")
app.include_router(book_router, prefix="/api")
app.include_router(graphql_router, prefix="")