# FastAPI GraphQL Example

## What is GraphQL?

GraphQL is a query language and runtime for APIs that allows clients to request exactly the data they need — nothing more, nothing less.  
Unlike REST APIs that expose multiple endpoints for different resources, GraphQL APIs typically expose a **single endpoint** and let the client specify the structure of the response.

### Key Benefits of GraphQL

- **Flexible data retrieval**: Clients choose the fields they want.
- **Reduced overfetching**: Only requested data is returned.
- **Single endpoint**: All queries and mutations are sent through one URL.

---

## How GraphQL is Implemented in This Project

This project is built with **FastAPI** and supports both **REST** and **GraphQL** APIs.

### GraphQL Setup Overview

- The **GraphQL API** is exposed at the [`/graphql`](http://localhost:8000/graphql) endpoint.
- The `ariadne` library is used to build the GraphQL schema and resolvers.

### File Structure and Responsibilities

- **GraphQL Controller**:  
  [`routers/graphql_router/graphql_controller.py`](routers/graphql_router/graphql_controller.py)  
  → Defines the GraphQL application and endpoint using `ariadne`'s ASGI integration.

- **Schema Definition**:  
  [`routers/graphql_router/schema.graphql`](routers/graphql_router/schema.graphql)  
  → Contains the GraphQL schema, including types, queries, and mutations.

- **Resolvers**:  
  [`routers/graphql_router/graphql_controller.py`](routers/graphql_router/graphql_controller.py)  
  → Connects GraphQL queries and mutations to resolver functions.

- **Mock Database**:  
  [`mock_db/database.py`](mock_db/database.py)  
  → Simulates a database for operations like fetching, creating, updating, and deleting books and authors.

- **Application Setup**:  
  [`main.py`](main.py)  
  → Mounts the GraphQL router alongside the REST routes.

```python
# main.py
from routers.graphql_router.graphql_controller import graphql_router

app.include_router(graphql_router, prefix="")
```

This setup makes the **GraphQL Playground** accessible directly at:  
[http://localhost:8000/graphql](http://localhost:8000/graphql) (when running locally).

## Supported GraphQL Operations

### Queries

- Fetch all books
- Fetch all authors
- Fetch a single book by ID
- Fetch a single author by ID

### Mutations

- Create a new book
- Update an existing book
- Delete a book

All these operations interact with the in-memory mock database located at:  
[`mock_db/database.py`](mock_db/database.py).