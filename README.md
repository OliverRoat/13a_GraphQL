# 13a [Individual] GraphQL

**Type**: Individual

Have a code example for the following [schema.graphql file](./schema.graphql).

### Criteria for completion

Recommended: Install any extension for syntax highlighting of `.graphql` files.

Implementing Subscription is optional.

The minimal requirement is that you should setup a server that can be queried through the GraphQL explorer, REST client (Postman) or a frontend.

### Choosing a library

As always, you can choose any library in any language (code-first or schema-first).

I have provided finished examples for Node (Apollo) and Python (Ariadne). You can bring them to the exam as long as you have a decent (not perfect) understanding of how they work.

If you implement your own version or expand on the provided templates then you are encouraged to use Copilot.

## How to use

```bash
$ poetry shell
$ poetry install --no-root
$ uvicorn main:app --reload
```
