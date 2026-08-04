# FastAPI And HTTP APIs

## What An API Is

An API is a controlled way for another program to interact with your app.

The client could be:

- browser;
- React frontend;
- Swagger docs;
- `curl`;
- Postman;
- automated tests;
- another backend service.

The server is the FastAPI app.

Analogy: restaurant ordering.

- Client: customer.
- Request: the order.
- Server: restaurant/kitchen.
- Route: where the order is sent.
- Request body: special instructions like "no onions."
- Response: the food or an explanation that the item is unavailable.

Important idea: the client does not directly call Python methods like `todolist.create_task()`. The client sends HTTP requests, and FastAPI maps those requests to Python functions.

## Request-Response Lifecycle

For `POST /tasks`, the flow is:

1. Client sends HTTP request with JSON.
2. FastAPI matches method and path to the route function.
3. Pydantic validates the request body.
4. Route function calls Python domain logic.
5. Domain logic returns a `Task`.
6. Route converts the `Task` into JSON-friendly data.
7. FastAPI sends JSON plus an HTTP status code.

Why this matters: an API request passes through layers. Each layer has a job.

## FastAPI App And Route Decorators

The app object:

```python
app = FastAPI()
```

Route decorators register functions with FastAPI:

```python
@app.get("/tasks")
def list_tasks():
    ...
```

Meaning:

```text
When a GET request comes to /tasks, run list_tasks().
```

The decorator connects HTTP to Python.

## Routes, Endpoints, And HTTP Methods

A route is the method/path combination:

```text
GET /tasks
POST /tasks
GET /tasks/{uid}
DELETE /tasks/{uid}
```

An endpoint is the Python function that handles the route.

HTTP methods describe intent:

- `GET`: read data;
- `POST`: create something;
- `PATCH`: partially update something;
- `DELETE`: remove something.

They do not enforce behavior automatically. Your Python code still decides what happens. But clients and developers expect these conventions.

## Visiting A URL Sends GET

Typing a URL into a browser usually sends a `GET` request.

That is why data-changing operations should not be implemented as `GET`.

Bad idea:

```text
GET /tasks/{uid}/delete
```

Better:

```text
DELETE /tasks/{uid}
```

What to remember: refreshing a page or visiting a link should not accidentally delete or create data.

## Path Parameters Vs Query Parameters

Path parameters identify a specific resource:

```text
/tasks/{uid}
/users/{user_id}
```

Query parameters usually filter, search, sort, or modify the request:

```text
/tasks?completed=false
/users?search=alex
```

For deleting one task, this is clearer:

```text
DELETE /tasks/{uid}
```

than:

```text
DELETE /tasks?uid=...
```

Rule: if the value identifies the thing, put it in the path. If it filters or modifies a request, put it in the query string.

## Request Bodies

A request body is structured data the client sends, usually JSON.

Example:

```json
{
  "title": "Buy milk",
  "description": "Whole milk"
}
```

`GET` usually does not have a body. `POST` and `PATCH` commonly do.

In this project, `POST /tasks` uses a request body to create a task.

## Serialization

Serialization means converting Python objects into a format that can be sent over the network.

Internal Python object:

```python
Task(...)
```

JSON-friendly API response:

```json
{
  "uid": "uuid-as-string",
  "title": "Buy milk",
  "description": "",
  "is_complete": false
}
```

Why this matters: clients do not understand custom Python objects. They understand JSON.

## FastAPI Response Conversion

FastAPI can automatically convert normal Python data into HTTP responses.

Example:

```python
@app.get("/example")
def example():
    return {"message": "hello"}
```

Response JSON:

```json
{
  "message": "hello"
}
```

FastAPI handles common values like dictionaries, lists, strings, numbers, booleans, `None`, and many standard types like `uuid.UUID`.

But raw custom objects are risky. When raw `Task` objects were returned, FastAPI exposed internal fields like `_title` and `_uid`.

What to remember: return intentional API-shaped data, not raw domain objects.

## `__repr__` Is Not An API Response

`__repr__` affects how objects print in Python.

FastAPI does not use `__repr__` as the API response shape.

This explained why:

- terminal output looked clean;
- API output exposed underscore-backed fields when raw objects were returned.

## FastAPI Automatic Docs

FastAPI generates interactive docs from route decorators, type hints, Pydantic models, and response models.

Local docs URL:

```text
http://127.0.0.1:8000/docs
```

Why this is useful:

- see available routes;
- test requests in the browser;
- inspect request body shapes;
- inspect response models;
- catch mismatch between expected and actual data.

## HTTP Status Codes

HTTP status codes tell the client what happened.

Important ones encountered:

- `200`: request succeeded.
- `404`: resource not found.
- `422`: request validation failed.
- `500`: unhandled server error.

Examples:

- invalid UUID path like `/tasks/not-a-uuid` returns `422` because FastAPI cannot parse the parameter as `uuid.UUID`;
- valid UUID format but missing task returns `404`;
- unhandled Python exceptions can become `500`.

## Python Exceptions Vs HTTP Errors

`TodoList` is plain Python code. It can raise Python exceptions:

```python
raise KeyError("Task does not exist")
```

The FastAPI route translates that into an HTTP response:

```python
from fastapi import HTTPException

try:
    task = todolist.get_task(uid)
except KeyError:
    raise HTTPException(status_code=404, detail="Task not found")
```

Why this matters: `TodoList` should not know about HTTP. The API layer knows how to communicate with HTTP clients.

