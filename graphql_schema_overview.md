# GraphQL Schema Overview

The `schema.graphql` file defines the **types**, **queries**, **mutations**, and **subscriptions** that structure the GraphQL API.

## Main Types

- **`Book`**  
  Represents a book with the following fields:
  - `id: ID!`
  - `title: String`
  - `release_year: Int`
  - `author_id: ID!`
  - `author: Author`

- **`Author`**  
  Represents an author:
  - `id: ID!`
  - `name: String`
  - `books: [Book]`

- **`ErrorMessage`**  
  Structure for returning error information:
  - `message: String`
  - `error_code: Int`

- **`SuccessMessage`**  
  Structure for returning a success response:
  - `message: String`

## Supported Queries

- `books`: Fetch all books.
- `book(id: ID!)`: Fetch a single book by its ID.
- `authors`: Fetch all authors.
- `author(id: ID!)`: Fetch a single author by their ID.

## Supported Mutations

- `createBook(title: String!, release_year: Int, author_id: ID!)`: Create a new book.
- `updateBook(id: ID!, title: String, release_year: Int, author_id: ID)`: Update an existing book.
- `deleteBook(id: ID!)`: Delete a book by its ID.

## Supported Subscriptions

- `bookAdded`: Subscribe to real-time updates when a new book is added.

# How the `schema.graphql` File Is Used

In this project, the `schema.graphql` file defines the structure of the GraphQL API separately from the business logic.

- The schema is **loaded** in [`routers/graphql_router/graphql_controller.py`](routers/graphql_router/graphql_controller.py).
- It is connected to **resolvers** using the [Ariadne](https://ariadnegraphql.org/) library.
- **Ariadne** uses the schema to validate incoming queries and connect them to Python resolver functions.

This setup makes it easier to maintain the API and ensures that:
- The schema defines **what operations are available**.
- The resolvers define **how those operations behave**.

The GraphQL Playground is accessible locally at:  
[`http://localhost:8000/graphql`](http://localhost:8000/graphql)