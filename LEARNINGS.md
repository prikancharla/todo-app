# Learnings

## Project Snapshot

This project is currently a small FastAPI backend for a todo app. The backend lives in `backend/`, uses `uv` for Python dependency management, and stores tasks in memory using a `TodoList` object containing `Task` objects. The API currently supports listing, creating, fetching, and deleting tasks. There is no database, frontend, Docker setup, or production deployment yet.

## Python And OOP

### Classes And Objects

A class is a blueprint for a type of thing. An object is one actual instance of that class.

In this project, `Task` represents one todo item. `TodoList` represents a collection of tasks and the behavior for managing that collection.

Key idea:

- `Task` should know how one task behaves.
- `TodoList` should know how a group of tasks is managed.

This is the basic object-oriented programming idea of putting related data and behavior together.

### Constructors And `self`

`__init__` is the constructor method Python calls when creating a new object.

```python
class Task:
    def __init__(self, title):
        self.title = title
```

`self` means "this specific object." If you create two tasks, each task has its own `self.title`.

Key lesson: constructor parameters are temporary inputs, while `self.some_name` stores data on the object.

### Attributes And Methods

An attribute is data stored on an object.

```python
task.title
task.is_complete
```

A method is behavior attached to an object.

```python
task.mark_complete()
task.toggle_complete()
```

Good class design usually asks: "What data does this object own, and what behavior belongs with that data?"

### `__repr__`, `__str__`, And Object Display

`__repr__` controls how an object is represented as text for developers.

Example:

```python
def __repr__(self):
    return f"Task(title={self.title!r}, is_complete={self.is_complete!r})"
```

When printing a list of objects, Python uses each object's `__repr__`.

```python
print([task])
```

This is why task output can look clean in the terminal even if the object's actual internal fields are named `_title`, `_description`, and `_is_complete`.

`!r` inside an f-string means "use the repr version of this value." This is useful for debugging because strings appear with quotes.

```python
title = "Buy milk"
print(f"{title}")   # Buy milk
print(f"{title!r}") # 'Buy milk'
```

`__str__` is usually for a more user-friendly display. `__repr__` is usually for a more developer/debug-oriented display.

Key lesson: `__repr__` helps with Python display and debugging. It does not define JSON output or API response shape.

### Getters, Setters, And Python Properties

Some languages commonly use explicit getter/setter methods:

```python
task.get_title()
task.set_title("Buy milk")
```

Python usually prefers direct-looking attribute access:

```python
task.title
task.title = "Buy milk"
```

But Python can still run getter/setter logic behind the scenes using `@property`.

```python
class Task:
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value
```

This gives a clean public interface while still protecting rules.

Key lesson: Python properties let code use `task.title` while the class still controls validation.

### Backing Fields And Internal Attributes

An attribute like `_title` is often called a backing field. It stores the actual value used by the public property `title`.

```python
self._title = value
```

The leading underscore means "internal implementation detail." It is a convention, not true privacy.

Key lesson: outside code should use `task.title`, not `task._title`, because `_title` is how the class happens to store the value internally.

### Setter Recursion Bug

Inside a setter, assigning to the public property calls the setter again.

Problem:

```python
@is_complete.setter
def is_complete(self, value):
    self.is_complete = value
```

This calls `is_complete` setter again and again.

Correct pattern:

```python
@is_complete.setter
def is_complete(self, value):
    self._is_complete = value
```

Key lesson: inside a setter, assign to the internal backing field.

### Encapsulation

Encapsulation means hiding internal details and exposing controlled ways to interact with an object.

Without encapsulation, outside code can put objects into invalid states:

```python
task._title = ""
todo_list.tasks["bad"] = "not a task"
```

With encapsulation, outside code uses controlled methods:

```python
task.title = "Buy milk"
todo_list.create_task("Buy milk")
todo_list.remove_task(uid)
```

Key lesson: encapsulation is not about hiding things for its own sake. It protects rules and keeps responsibilities clear.

### Dataclasses

`@dataclass` is a decorator that can automatically generate common class boilerplate such as an initializer and readable representation.

Example:

```python
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    description: str = ""
    is_complete: bool = False
```

This automatically gives the class an `__init__` similar to:

```python
Task(title, description="", is_complete=False)
```

Why it is useful:

- Less repetitive code.
- Good for simple data containers.
- Automatically gives helpful display/debug behavior.

Why we moved away from it for now:

- We wanted to practice manual constructors.
- We added validation through property setters.
- The class started becoming more than a passive data container.

Key lesson: dataclasses are useful when a class mostly stores data. Manual classes are useful when you want to deeply control initialization, validation, and behavior.

### Decorators

A decorator is syntax that wraps, modifies, or registers a function or class.

General shape:

```python
@some_decorator
def some_function():
    ...
```

Conceptually, the decorator changes how the function/class behaves or how another system sees it.

Examples encountered:

- `@dataclass`: modifies a class by generating common methods.
- `@property`: makes a method accessible like an attribute.
- `@title.setter`: registers the setter for the `title` property.
- `@app.get("/tasks")`: registers a function as a FastAPI route.
- `@app.post("/tasks")`: registers a function as a POST endpoint.

Key lesson: decorators are not comments. They actively change or register behavior.

### Type Hints Vs Runtime Validation

Type hints describe expected types:

```python
def __init__(self, title: str):
    ...
```

But Python does not automatically enforce them at runtime.

This can still be called unless validation rejects it:

```python
Task(123)
```

Runtime validation is explicit code:

```python
if not isinstance(value, str):
    raise TypeError("Title should be a string")
```

Key lesson: type hints help humans and tools; validation protects runtime behavior.

### Optional Types Vs Default Values

`Optional[str]` means the value may be either `str` or `None`.

```python
description: Optional[str]
```

This does not automatically mean the argument can be omitted. A default value makes it optional to pass.

```python
description: Optional[str] = None
description: str = ""
```

These mean different things:

- `Optional[str] = None`: value may be missing or explicitly `None`.
- `str = ""`: value should be a string, and empty string means no description.

Key lesson: "optional type" and "optional argument" are related but not the same.

### Positional Vs Keyword Arguments

Python binds positional arguments left to right.

```python
def __init__(self, title, description="", is_complete=False):
    ...
```

This call:

```python
Task("Buy milk", "Get whole milk")
```

means:

```python
title = "Buy milk"
description = "Get whole milk"
```

Keyword arguments target names directly:

```python
Task("Buy milk", is_complete=True)
```

Key lesson: once a function has multiple optional parameters, keyword arguments are clearer and less error-prone.

### Python Modules And Imports

A `.py` file is a Python module.

```text
todo.py -> module named todo
main.py -> module named main
```

This import:

```python
from todo import TodoList
```

means "from the `todo.py` module, import `TodoList`."

Where Python is run from matters. Running FastAPI from inside `backend/` lets Python find `todo.py` next to `main.py`.

Key lesson: imports depend on project structure and Python's module search path.

### `if __name__ == "__main__"`

This block runs only when a file is executed directly:

```python
if __name__ == "__main__":
    main()
```

It does not run when the file is imported by another file.

Why it matters:

- It is useful for quick manual testing.
- It keeps demo/playground code from running when another module imports the file.
- It lets `todo.py` be both a reusable module and a directly runnable script.

Key lesson: code under `if __name__ == "__main__"` is a safe place for temporary manual experiments.

## Data Modeling And Design Decisions

### `Task` And `TodoList` Responsibilities

The current model has two main classes:

- `Task`: stores task data and validates fields.
- `TodoList`: stores multiple tasks and provides operations like create, get, list, remove, and toggle.

Key lesson: a single object should not do everything. `Task` should not manage the whole collection, and `TodoList` should not contain all field validation details for a task.

### ID Ownership

One recurring design question was: who creates task IDs?

Options:

- Caller creates the ID.
- `Task` creates its own ID.
- `TodoList` assigns the ID.
- A future database assigns the ID.

Current decision: `Task` currently creates its own UUID, and `TodoList` indexes tasks by that UUID.

Tradeoff:

- UUIDs are realistic and globally unique.
- Integer IDs are easier to read and common in SQL databases.
- Later, a database may take over ID generation.

Key lesson: only one layer should own ID generation at a time, otherwise duplicate IDs and unclear responsibility become likely.

### Lists Vs Dictionaries

A list is simple:

```python
tasks = [task1, task2]
```

But finding one task by ID requires scanning the list.

A dictionary is better for lookup:

```python
tasks = {
    task.uid: task
}
```

Current decision: `TodoList` stores tasks in a dictionary keyed by UUID.

Key lesson: data structure choice affects how easy operations like lookup, delete, and update become.

### Returning Internal Storage

Returning the raw internal dictionary would expose the implementation:

```python
return self.tasks
```

Returning a list hides how tasks are stored:

```python
return list(self.tasks.values())
```

Key lesson: outside code should ask for tasks, not depend on whether they are stored in a dictionary, list, or database.

### Toggle Vs Explicit Set

`toggle_complete()` flips the current state.

```python
False -> True
True -> False
```

This matches a checkbox UI, where the user can check and uncheck.

But APIs often prefer explicit updates:

```json
{
  "is_complete": true
}
```

Tradeoff:

- Toggle is simple and maps to the current method.
- Explicit set is safer because repeated requests produce the same final state.

Key lesson: UI behavior and API design are related, but not always identical.

## FastAPI And HTTP APIs

### What An API Is

An API is a controlled way for another program to interact with your app.

The client might be:

- A React frontend.
- A browser.
- Postman.
- `curl`.
- Another backend service.
- Automated tests.

Key lesson: an API is not only for a UI. It is a contract for any HTTP client.

### Client-Server Model

A client asks for something. A server receives the request, does work, and sends back a response.

Restaurant analogy:

- Client: customer.
- Request: order placed with the waiter.
- Server: kitchen/restaurant system.
- Route: the counter or menu path where the order goes.
- Request body: details like "no onions."
- Response: the prepared food or an explanation that the item is unavailable.

In this project:

- Client: browser, Swagger docs, frontend, `curl`, Postman, or tests.
- Server: FastAPI app.
- Request: `GET /tasks`, `POST /tasks`, `DELETE /tasks/{uid}`.
- Response: JSON plus an HTTP status code.

Key lesson: the client does not directly call Python methods like `todolist.create_task()`. It sends HTTP requests. FastAPI translates those requests into Python function calls.

### Request-Response Lifecycle

A typical request flow:

1. Client sends `POST /tasks` with JSON.
2. FastAPI matches the request to the `POST /tasks` route.
3. Pydantic validates the request body.
4. The route function calls domain logic such as `todolist.create_task(...)`.
5. The domain object returns a `Task`.
6. The route serializes the task into JSON-friendly data.
7. FastAPI sends response JSON and an HTTP status code.

Key lesson: an API request passes through several layers. Each layer has a different responsibility.

### FastAPI App And Route Decorators

FastAPI starts with an app object:

```python
app = FastAPI()
```

Route decorators connect HTTP requests to Python functions:

```python
@app.get("/tasks")
def list_tasks():
    ...
```

This means: when the server receives `GET /tasks`, run `list_tasks`.

Key lesson: FastAPI uses the HTTP method and path together to choose the route function.

### Endpoints And Routes

A route is the API path and method combination.

Examples:

```text
GET /tasks
POST /tasks
GET /tasks/{uid}
DELETE /tasks/{uid}
```

An endpoint is the function that handles that route.

Key lesson: the same path can support different actions if the HTTP method is different.

### HTTP Methods

HTTP methods describe what kind of operation the client wants.

- `GET`: read data.
- `POST`: create something.
- `PATCH`: partially update something.
- `DELETE`: remove something.

These methods do not magically enforce the behavior. The Python code still controls what happens. But they create a shared convention between client and server.

Key lesson: `GET /tasks` and `POST /tasks` can share the same path but mean different things.

### Visiting A URL Usually Sends GET

Typing a URL into a browser address bar usually sends a `GET` request.

This is why data-changing actions should not be implemented as GET routes.

Bad idea:

```text
GET /tasks/{uid}/delete
```

Better:

```text
DELETE /tasks/{uid}
```

Key lesson: refreshing or visiting a URL should not accidentally create, update, or delete data.

### Path Parameters Vs Query Parameters

A path parameter identifies a specific resource:

```text
/tasks/{uid}
/users/{user_id}
```

A query parameter filters, searches, sorts, or modifies a request:

```text
/tasks?completed=false
/users?search=alex
```

For deleting one task:

```text
DELETE /tasks/{uid}
```

is clearer than:

```text
DELETE /tasks?uid=...
```

Key lesson: if the value identifies the thing, put it in the path. If it filters or modifies a request, put it in the query string.

### Request Bodies

A request body is data sent by the client, usually JSON.

Example for creating a task:

```json
{
  "title": "Buy milk",
  "description": "Whole milk"
}
```

`GET` requests usually do not have bodies. `POST` and `PATCH` commonly do.

Key lesson: request bodies are how clients send structured data to the API.

### Serialization

Serialization means converting internal Python objects into a format that can be sent over the network, usually JSON.

Internal object:

```python
Task(...)
```

JSON-friendly response:

```json
{
  "uid": "uuid-as-string",
  "title": "Buy milk",
  "description": "",
  "is_complete": false
}
```

Key lesson: API responses should not return raw domain objects directly.

### FastAPI Response Conversion

FastAPI route functions can return normal Python data such as dictionaries, lists, strings, numbers, booleans, and `None`. FastAPI converts these into HTTP responses, usually JSON.

Example:

```python
@app.get("/example")
def example():
    return {"message": "hello"}
```

The HTTP response body becomes JSON:

```json
{
  "message": "hello"
}
```

FastAPI can also handle many common Python types, such as `uuid.UUID`, by converting them into JSON-compatible values.

However, custom domain objects like `Task` are not ideal API responses. FastAPI may inspect their internal attributes, which can expose implementation details like `_title`, `_description`, or `_uid`.

Better route behavior:

```python
return {
    "uid": str(task.uid),
    "title": task.title,
    "description": task.description,
    "is_complete": task.is_complete,
}
```

Key lesson: FastAPI can convert many values automatically, but route functions should still return intentional API-shaped data instead of raw domain objects.

### `__repr__` Is Not An API Response

`__repr__` controls how an object appears when printed in Python.

FastAPI does not use `__repr__` as the API response format. When raw objects were returned, FastAPI exposed internal fields like `_title` and `_uid`.

Key lesson: printing/debug display and JSON serialization are different concerns.

### FastAPI Automatic Docs

FastAPI generates interactive API documentation from route definitions, type hints, Pydantic models, and response models.

Common docs URL while developing locally:

```text
http://127.0.0.1:8000/docs
```

Why it matters:

- You can inspect available routes.
- You can send test requests from the browser.
- You can see request and response shapes.
- It helps catch mismatches between what the API expects and what the client sends.

Key lesson: FastAPI documentation is generated from the code, so clearer route types and Pydantic models produce clearer API docs.

### HTTP Status Codes

Status codes tell the client what happened.

- `200`: success.
- `404`: requested resource was not found.
- `422`: request validation failed, often from FastAPI/Pydantic.
- `500`: unhandled backend error.

Key lesson: status codes are part of the API contract. Clients should not have to parse Python exception text to understand what happened.

### Python Exceptions Vs HTTP Errors

The domain layer may raise Python exceptions:

```python
raise KeyError("Task does not exist")
```

The FastAPI layer should translate relevant exceptions into HTTP errors:

```python
from fastapi import HTTPException

try:
    task = todolist.get_task(uid)
except KeyError:
    raise HTTPException(status_code=404, detail="Task not found")
```

Key lesson: keep HTTP-specific errors in the API layer, not inside plain Python domain classes like `TodoList`.

### 404 Vs 422 In FastAPI

Two different error cases can happen with a route like:

```text
GET /tasks/{uid}
```

If the client sends something that is not a valid UUID:

```text
GET /tasks/not-a-uuid
```

FastAPI rejects it before the route logic runs because the path parameter cannot be parsed as `uuid.UUID`. That produces a validation error, typically `422`.

If the client sends a valid UUID format, but no task exists with that ID:

```text
GET /tasks/00000000-0000-0000-0000-000000000000
```

the route runs, `TodoList` raises `KeyError`, and the route should translate that into:

```python
raise HTTPException(status_code=404, detail="Task not found")
```

Key lesson: `422` means the request shape/type was invalid. `404` means the request was understandable, but the requested resource does not exist.

## Pydantic And Validation

### What Pydantic Does In FastAPI

Pydantic defines the expected shape of data and validates it.

In FastAPI, Pydantic is commonly used for:

- Request bodies.
- Response models.
- Type validation.
- Automatic API documentation.

Key lesson: Pydantic models are API data shapes, not necessarily the same thing as domain classes.

### Request Models

A request model describes what the client is allowed or required to send.

Example:

```python
class InputTaskData(BaseModel):
    title: str
    description: str = ""
```

This says:

- `title` is required.
- `description` is optional to pass because it has a default.
- both fields should be strings.

FastAPI uses this model to parse and validate the request body before the route logic runs.

Key lesson: request models protect the boundary between outside clients and your application code.

### Response Models

A response model describes what the API returns.

Example:

```python
class OutputTaskData(BaseModel):
    uid: str
    title: str
    description: str
    is_complete: bool
```

The response can include fields the client did not send, such as:

- `uid`: generated by the server.
- `is_complete`: defaulted by the server.

Key lesson: input and output shapes are often different.

### `response_model` As An API Contract

In FastAPI, `response_model` tells FastAPI and API clients what shape a route should return.

Example:

```python
@app.get("/tasks", response_model=list[OutputTaskData])
def list_tasks():
    ...
```

Why it matters:

- It documents the response shape in `/docs`.
- It helps FastAPI validate/filter returned data.
- It communicates what clients can rely on.

Key lesson: `response_model` is not just decoration. It is part of the API contract.

### What `response_model` Does And Does Not Do

`response_model` can validate, document, filter, and serialize returned data.

It can filter out extra fields that are not part of the response model.

Example:

```python
class PublicTask(BaseModel):
    title: str


@app.get("/task", response_model=PublicTask)
def get_task():
    return {
        "title": "Buy milk",
        "internal_note": "do not expose this",
    }
```

The API response only includes:

```json
{
  "title": "Buy milk"
}
```

This is useful, but it should not become an excuse to return messy internal objects everywhere. It is still better to intentionally convert domain objects into clear API response shapes.

What `response_model` does:

- Documents the expected response in `/docs`.
- Validates that returned data matches the expected shape.
- Filters out fields not included in the model.
- Helps serialize returned data into JSON-compatible output.

What `response_model` does not do:

- It does not automatically make domain object design clean.
- It does not replace careful API boundary design.
- It does not mean clients should see internal object attributes.

Key lesson: `response_model` is a contract and safety net. Explicit serialization keeps the boundary between domain objects and API responses clearer.

### Optional Fields In Pydantic

This means the field type allows `None`, but the field may still be required depending on the Pydantic version and defaults:

```python
description: Optional[str]
```

This clearly makes the field omittable:

```python
description: Optional[str] = None
```

This says the field is always a string if present, with a default:

```python
description: str = ""
```

Key lesson: use defaults intentionally. Type optionality and field requiredness are different concepts.

### Model To Dictionary Conversion

Pydantic models can be converted into dictionaries.

Older style:

```python
input_task.dict()
```

Newer style:

```python
input_task.model_dump()
```

This is useful when passing validated data into regular Python functions.

Key lesson: Pydantic models are objects, but sometimes normal dictionaries are easier for integration.

### Dictionary Unpacking With `**`

`**` unpacks dictionary keys into keyword arguments.

```python
data = {
    "title": "Buy milk",
    "description": "Whole milk",
}

todolist.create_task(**data)
```

This is equivalent to:

```python
todolist.create_task(title="Buy milk", description="Whole milk")
```

Key lesson: dictionary keys must match the target function's parameter names.

## Dependency Management

### Why Use A Virtual Environment

A virtual environment isolates packages for one project.

Without it, packages installed for one project can interfere with another project.

Current decision: the backend has a `.venv/` managed by `uv`.

Key lesson: the virtual environment is local machine state and should not be committed.

### `uv`

`uv` manages Python dependencies and project environments.

Useful commands:

```bash
uv init --bare
uv add "fastapi[standard]"
uv run fastapi dev main.py
```

Why it matters:

- dependencies are recorded in the project.
- commands run in the project environment.
- setup is easier to reproduce later.

### `pyproject.toml` And `uv.lock`

`pyproject.toml` records project metadata and direct dependencies.

`uv.lock` records exact resolved dependency versions.

Current decision:

- Commit `backend/pyproject.toml`.
- Commit `backend/uv.lock`.
- Do not commit `backend/.venv/`.

Key lesson: commit dependency definitions and lockfiles, not installed package folders.

### How To Approach A New Library

A practical learning loop for a new library:

1. Identify why the library is needed.
2. Install it in the project environment.
3. Import the smallest needed piece.
4. Build the smallest working example.
5. Verify it runs.
6. Add one feature at a time.

Example with FastAPI:

- Need: expose Python logic over HTTP.
- Install: `uv add "fastapi[standard]"`.
- Import: `from fastapi import FastAPI`.
- Smallest app: one `GET /` route.
- Verify: open `/docs`.

Key lesson: do not start with the whole documentation surface. First prove the smallest useful path works.

## Project Organization

### Why Folder Structure Evolves

Small projects can start with a few files. Larger projects split files by responsibility.

Early structure:

```text
backend/
  main.py
  todo.py
```

Possible later structure:

```text
backend/
  app/
    main.py
    domain/
    schemas/
    api/
    repositories/
    db/
  tests/
```

The goal is not to create folders for appearance. The goal is to reduce confusion when files become too large or responsibilities mix.

Key lesson: split code when there is real pressure, such as repeated schemas, many routes, database code, or tests.

### Common Backend Folders

Common folder responsibilities:

- `domain/`: business concepts like `Task` and `TodoList`.
- `schemas/`: Pydantic request/response models.
- `api/` or `routes/`: FastAPI route functions.
- `repositories/`: data access logic.
- `db/`: database connection/session/table setup.
- `tests/`: automated tests.

Key lesson: folder names should communicate responsibility.

### Generated Files And `.gitignore`

Some files are source code and should be committed. Others are generated by tools and should be ignored.

Usually commit:

- `.py` source files.
- `pyproject.toml`.
- `uv.lock`.

Usually ignore:

- `.venv/`.
- `__pycache__/`.
- `.pyc` files.

Key lesson: commit files needed to reproduce the project, not machine-local generated output.

## Current Design Decisions

### Keep The Backend Simple For Now

The project currently keeps `main.py` and `todo.py` simple rather than splitting into many folders.

This is intentional because the project is still small.

Expected future pressure:

- multiple routes may motivate route modules.
- repeated schemas may motivate a schemas file.
- database persistence may motivate repository/database modules.

Key lesson: split files when the code gives a reason, not just to imitate a large app.

### Single Global TodoList

The backend currently uses one global in-memory `TodoList`.

This means:

- data resets when the server restarts.
- all users would share the same list.
- it is fine for learning FastAPI basics.

Key lesson: in-memory state is useful for learning but not real persistence.

## Deferred Topics

These topics have been discussed but not implemented deeply yet. They should be expanded when the project actually reaches them.

- Docker.
- Backend deployment.
- Vercel frontend deployment.
- SQL Server persistence.
- React frontend.
- Unit tests and API tests.
- CI/CD.
