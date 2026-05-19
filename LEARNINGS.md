# Learnings

## How To Use This File

This file is a study guide for the todo app project. It is organized by concept, not by date. The goal is to help you return to the project later and remember:

- what each technology or concept means;
- why we used it;
- how it appears in this project;
- what commands matter;
- what files are important;
- what mistakes or tradeoffs came up.

This file should not record every small code edit. It should preserve high-value concepts that are likely to matter again.

## Project Snapshot

The project is currently a small FastAPI backend for a todo app.

Current repo shape:

```text
todo-app/
  AGENTS.md
  LEARNINGS.md
  backend/
    main.py
    todo.py
    pyproject.toml
    uv.lock
```

Current backend:

- `backend/todo.py` contains plain Python domain classes: `Task` and `TodoList`.
- `backend/main.py` contains the FastAPI app, Pydantic request/response models, and API routes.
- Dependencies are managed with `uv`.
- Data is stored in memory in one global `TodoList`, so data resets when the app restarts.

Current API capabilities:

```text
GET    /tasks
POST   /tasks
GET    /tasks/{uid}
DELETE /tasks/{uid}
PATCH  /tasks/{uid}/toggle
```

Known limitations:

- No database yet.
- No frontend yet.
- No Docker image completed yet.
- No production deployment yet.
- All users would currently share the same in-memory todo list.

## Python Fundamentals And OOP

### Classes And Objects

A class is a blueprint. An object is one actual thing made from that blueprint.

Example:

```python
class Task:
    ...

task = Task("Buy milk")
```

`Task` is the class. `task` is one object.

In this project:

- `Task` represents one todo item.
- `TodoList` represents a collection of tasks and operations on that collection.

Why this matters: object-oriented programming is about grouping related data and behavior together. A `Task` should know about one task's fields and behavior. A `TodoList` should know how to manage multiple tasks.

### Constructors And `self`

`__init__` is the constructor method. Python calls it when creating a new object.

```python
class Task:
    def __init__(self, title):
        self.title = title
```

`self` means "this specific object."

If you create two tasks:

```python
task1 = Task("Buy milk")
task2 = Task("Call dentist")
```

each object has its own `self.title`.

Key idea:

- `title` is a temporary input passed into the constructor.
- `self.title` stores data on the object.

### Attributes And Methods

An attribute is data on an object.

```python
task.title
task.description
task.is_complete
```

A method is behavior attached to an object.

```python
task.mark_complete()
task.toggle_complete()
```

Good design question: does this behavior belong to one task or to the collection of tasks?

Examples:

- `Task.toggle_complete()` belongs to one task.
- `TodoList.get_task(uid)` belongs to the collection because it finds a task by ID.

### Getters, Setters, And Python Properties

Some languages use explicit getter and setter methods:

```python
task.get_title()
task.set_title("Buy milk")
```

Python usually prefers direct-looking attribute access:

```python
task.title
task.title = "Buy milk"
```

But direct-looking access can still run logic through `@property`.

Example:

```python
class Task:
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title should be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value
```

What happens:

- Reading `task.title` calls the getter.
- Assigning `task.title = "Buy milk"` calls the setter.
- The actual stored value is `task._title`.

Why this matters: properties let the class expose a clean public interface while still enforcing rules.

### Backing Fields And Internal Attributes

`_title`, `_description`, and `_is_complete` are backing fields. They store values internally.

The leading underscore is a Python convention:

```text
This is internal. Do not use it directly from outside the class.
```

It is not hard privacy. Python will still let you access `_title`, but the convention matters.

Use:

```python
task.title
```

Avoid:

```python
task._title
```

Why this matters: if outside code depends on internal fields, it becomes harder to change how the class works later.

### Setter Recursion Bug

Inside a setter, assigning to the public property calls the setter again.

Problem:

```python
@is_complete.setter
def is_complete(self, value):
    self.is_complete = value
```

This calls the same setter repeatedly.

Correct pattern:

```python
@is_complete.setter
def is_complete(self, value):
    self._is_complete = value
```

What to remember: setters should usually validate input, then assign to the internal backing field.

### Encapsulation

Encapsulation means hiding internal details and exposing controlled ways to interact with an object.

Without encapsulation:

```python
task._title = ""
todo_list.tasks["bad"] = "not a task"
```

With encapsulation:

```python
task.title = "Buy milk"
todo_list.create_task("Buy milk")
todo_list.remove_task(uid)
```

Why this matters: encapsulation protects rules. For example:

- a task title should not be empty;
- `is_complete` should be a boolean;
- the todo list should only contain `Task` objects;
- outside code should not directly mutate the internal task dictionary.

### Dataclasses

`@dataclass` is a decorator that can generate common class boilerplate.

Example:

```python
from dataclasses import dataclass

@dataclass
class Task:
    title: str
    description: str = ""
    is_complete: bool = False
```

This gives you an initializer automatically:

```python
Task(title, description="", is_complete=False)
```

Why dataclasses are useful:

- less repetitive constructor code;
- readable debug output;
- good for simple data containers.

Why we moved away from it:

- we wanted to learn manual class construction;
- we needed validation through properties/setters;
- `Task` became more than just passive data.

What to remember: dataclasses are good when a class mostly stores data. Manual classes are useful when you want more control over validation and behavior.

### Decorators

A decorator is syntax that modifies, wraps, or registers a function or class.

General shape:

```python
@some_decorator
def some_function():
    ...
```

Decorators are not comments. They affect behavior.

Examples encountered:

- `@dataclass`: modifies a class by generating methods.
- `@property`: makes a method look like an attribute.
- `@title.setter`: registers the setter for a property.
- `@app.get("/tasks")`: registers a FastAPI route for `GET /tasks`.
- `@app.post("/tasks")`: registers a FastAPI route for `POST /tasks`.

What to remember: decorators often connect your code to a framework or language feature.

### Type Hints Vs Runtime Validation

Type hints describe expected types:

```python
def __init__(self, title: str):
    ...
```

But Python does not automatically enforce them at runtime.

This can still be called unless your code rejects it:

```python
Task(123)
```

Runtime validation is explicit:

```python
if not isinstance(value, str):
    raise TypeError("Title should be a string")
```

What to remember:

- Type hints help humans, editors, and type checkers.
- Validation protects the running program.

### Optional Types Vs Default Values

`Optional[str]` means a value may be either `str` or `None`.

```python
description: Optional[str]
```

That does not automatically mean the argument may be omitted. A default value makes an argument optional to pass.

Examples:

```python
description: Optional[str] = None
description: str = ""
```

Meaning:

- `Optional[str] = None`: the value can be a string or `None`; if omitted, it defaults to `None`.
- `str = ""`: the value should be a string; if omitted, it defaults to an empty string.

This came up in both Python classes and Pydantic models.

What to remember: optional type and optional argument are related but not the same thing.

### Positional Vs Keyword Arguments

Python binds positional arguments left to right.

```python
def __init__(self, title, description="", is_complete=False):
    ...
```

This:

```python
Task("Buy milk", "Get whole milk")
```

means:

```python
title = "Buy milk"
description = "Get whole milk"
```

Keyword arguments target parameter names:

```python
Task("Buy milk", is_complete=True)
```

What to remember: once a function has multiple optional parameters, keyword arguments are clearer and safer.

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

`!r` inside an f-string means "use the repr version of this value."

```python
title = "Buy milk"
print(f"{title}")    # Buy milk
print(f"{title!r}")  # 'Buy milk'
```

`__str__` is usually for user-friendly display. `__repr__` is usually for developer/debug display.

Important distinction: `__repr__` is not JSON serialization. It made task output look clean in the terminal, but FastAPI still exposed internal fields when raw `Task` objects were returned.

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

means: from the `todo.py` module, import `TodoList`.

Where you run Python from matters. Running FastAPI from inside `backend/` lets Python find `todo.py` next to `main.py`.

What to remember: imports depend on project structure and Python's module search path.

### `if __name__ == "__main__"`

This block runs only when a file is executed directly:

```python
if __name__ == "__main__":
    main()
```

It does not run when another file imports the module.

Why this matters:

- useful for quick manual testing;
- keeps playground/demo code from running during imports;
- lets `todo.py` be both importable and directly runnable.

## Backend Domain Design

### `Task` And `TodoList` Responsibilities

Current design:

- `Task`: stores one task's data and validates fields.
- `TodoList`: stores multiple tasks and provides collection operations.

Examples:

- `Task.toggle_complete()` changes one task.
- `TodoList.get_task(uid)` finds one task from the collection.
- `TodoList.remove_task(uid)` removes one task from the collection.

Why this matters: classes should have focused responsibilities. If every class knows everything, the code becomes hard to change.

### ID Ownership

We discussed several possible owners for task IDs:

- caller provides IDs;
- `Task` creates its own ID;
- `TodoList` assigns IDs;
- a future database assigns IDs.

Current decision: `Task` creates its own UUID, and `TodoList` stores tasks by UUID.

Why UUIDs:

- globally unique;
- easy to generate without a database;
- useful for API URLs.

Tradeoff:

- UUIDs are harder to read than integers;
- SQL databases often use integer primary keys;
- future database integration may change ID ownership.

What to remember: only one layer should own ID generation at a time.

### Lists Vs Dictionaries

A list is simple:

```python
tasks = [task1, task2]
```

But finding a task by ID requires scanning the list.

A dictionary is better for direct lookup:

```python
tasks = {
    task.uid: task
}
```

Current design: `TodoList` stores tasks in a dictionary keyed by UUID.

Why this matters:

- `get_task(uid)` can look up directly by ID;
- `remove_task(uid)` can delete directly by ID;
- API routes naturally work with IDs.

### Returning Internal Storage

Returning the raw internal dictionary exposes implementation details:

```python
return self.tasks
```

Returning a list hides the storage choice:

```python
return list(self.tasks.values())
```

Why this matters: outside code should not depend on whether tasks are stored in a dictionary, list, or database.

## FastAPI And HTTP APIs

### What An API Is

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

### Request-Response Lifecycle

For `POST /tasks`, the flow is:

1. Client sends HTTP request with JSON.
2. FastAPI matches method and path to the route function.
3. Pydantic validates the request body.
4. Route function calls Python domain logic.
5. Domain logic returns a `Task`.
6. Route converts the `Task` into JSON-friendly data.
7. FastAPI sends JSON plus an HTTP status code.

Why this matters: an API request passes through layers. Each layer has a job.

### FastAPI App And Route Decorators

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

### Routes, Endpoints, And HTTP Methods

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

### Visiting A URL Sends GET

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

### Path Parameters Vs Query Parameters

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

### Request Bodies

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

### Serialization

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

### FastAPI Response Conversion

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

### `__repr__` Is Not An API Response

`__repr__` affects how objects print in Python.

FastAPI does not use `__repr__` as the API response shape.

This explained why:

- terminal output looked clean;
- API output exposed underscore-backed fields when raw objects were returned.

### FastAPI Automatic Docs

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

### HTTP Status Codes

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

### Python Exceptions Vs HTTP Errors

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

## Pydantic And Validation

### What Pydantic Does

Pydantic validates and structures data.

FastAPI uses Pydantic for:

- request bodies;
- response models;
- automatic docs;
- type conversion and validation.

Important distinction:

- `Task` is a domain class with behavior.
- `InputTaskData` is an API request shape.
- `OutputTaskData` is an API response shape.

These are related, but they are not the same thing.

### Request Models

A request model describes what the client sends.

Example:

```python
class InputTaskData(BaseModel):
    title: str
    description: str = ""
```

Meaning:

- `title` is required;
- `description` can be omitted because it has a default;
- both should be strings.

FastAPI uses this to validate incoming JSON before route logic runs.

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

Why output can include more fields than input:

- client does not send `uid`; server creates it;
- client does not send `is_complete`; server defaults it.

Input shape and output shape often differ.

### `response_model`

FastAPI routes can declare a response model:

```python
@app.get("/tasks", response_model=list[OutputTaskData])
def list_tasks():
    ...
```

What it does:

- documents the response shape in `/docs`;
- validates returned data;
- filters out fields not in the response model;
- helps serialize output.

Example of filtering:

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

Response:

```json
{
  "title": "Buy milk"
}
```

What to remember: `response_model` is a contract and safety net. It does not replace careful API boundary design.

### Optional Fields And Defaults In Pydantic

These mean different things:

```python
description: Optional[str]
description: Optional[str] = None
description: str = ""
```

Meaning:

- `Optional[str]`: type allows `None`, but field may still be required depending on defaults/version behavior.
- `Optional[str] = None`: field can be omitted and defaults to `None`.
- `str = ""`: field can be omitted and defaults to an empty string.

What to remember: default values determine whether the client can omit a field.

### Model To Dictionary Conversion

Pydantic model objects can be converted into dictionaries.

Older/common style:

```python
input_task.dict()
```

Newer Pydantic v2 style:

```python
input_task.model_dump()
```

This is useful when passing validated data into normal Python functions.

### Dictionary Unpacking With `**`

`**` unpacks a dictionary into keyword arguments.

```python
data = {
    "title": "Buy milk",
    "description": "Whole milk",
}

todolist.create_task(**data)
```

Equivalent:

```python
todolist.create_task(title="Buy milk", description="Whole milk")
```

Requirement: dictionary keys must match the function parameter names.

## Dependency Management With uv

### The Problem uv Solves

Python projects usually depend on external packages. This backend needs packages like FastAPI and Pydantic.

Bad habit:

```bash
pip install fastapi
```

without knowing where it installs. It might install globally or into whichever virtual environment happens to be active.

Better approach:

```text
The backend declares its dependencies, locks exact versions, and runs commands inside an isolated environment.
```

`uv` helps manage that workflow.

### How uv, pyproject.toml, uv.lock, And .venv Fit Together

`uv` is the tool.

`pyproject.toml` is the dependency/config declaration.

`uv.lock` is the exact resolved dependency lockfile.

`.venv/` is the installed local environment.

Relationship:

```text
uv reads pyproject.toml
uv resolves exact package versions
uv writes uv.lock
uv installs packages into .venv/
uv run executes commands using that environment
```

Another way to remember it:

```text
pyproject.toml says what the project needs
uv.lock says exactly what versions were chosen
.venv contains the installed packages
uv is the command that manages all of this
```

### Why The Files Are Inside backend/

The repo will eventually have both backend and frontend code.

Python dependencies belong to the backend:

```text
backend/
  pyproject.toml
  uv.lock
  .venv/
```

Later, frontend dependencies will likely belong in:

```text
frontend/
  package.json
  package-lock.json or similar
```

Why this matters: backend Python dependencies and frontend JavaScript dependencies should be managed separately.

### pyproject.toml

`pyproject.toml` is a standard Python project configuration file.

In this project:

```text
backend/pyproject.toml
```

Example:

```toml
[project]
name = "backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.136.1",
    "pydantic>=2.13.3",
]
```

Meaning:

- `[project]`: Python project metadata section.
- `name`: project name.
- `version`: project version.
- `requires-python`: compatible Python version range.
- `dependencies`: packages the project needs.

How it is tied to `uv`: when you run `uv add`, `uv` updates the `dependencies` list in `pyproject.toml`.

### What TOML Is

TOML is a configuration file format.

It is designed to be readable:

```toml
name = "backend"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.136.1",
]
```

Common TOML ideas:

- `key = value` sets a value;
- `[section]` creates a table/section;
- lists use square brackets.

`pyproject.toml` uses TOML syntax because Python tooling standardized around this file format for project configuration.

### uv.lock

`uv.lock` records the exact dependency solution.

If `pyproject.toml` says:

```text
fastapi >= 0.136.1
```

there may be many valid FastAPI versions and many sub-dependency versions. `uv.lock` records the exact versions selected.

Why commit it:

- another machine can install the same versions;
- Docker builds can reproduce the same environment;
- deployment can use the same dependency set;
- fewer surprises from dependency updates.

What to remember: `pyproject.toml` is the human-facing dependency declaration. `uv.lock` is the exact machine-resolved result.

### .venv

`.venv/` is the actual virtual environment folder.

It contains installed packages and Python environment files.

Do not commit it because:

- it is machine-specific;
- it can be recreated from `pyproject.toml` and `uv.lock`;
- it can be large;
- it may differ across operating systems and CPU architectures.

### Commands We Used

Run backend Python commands from:

```bash
cd backend
```

Why: `uv` looks for `pyproject.toml` in the current directory or parent directories. Since the backend Python project is in `backend/`, run backend commands there.

Initialize the backend project:

```bash
uv init --bare
```

What it does:

- creates a minimal `pyproject.toml`;
- does not create extra sample source files because of `--bare`.

Why `--bare`: we already had backend files and did not want generated starter files.

Add FastAPI:

```bash
uv add "fastapi[standard]"
```

What it does:

- updates `pyproject.toml`;
- resolves exact dependency versions;
- updates `uv.lock`;
- installs/syncs packages into `.venv/`.

Why quotes: some shells can treat square brackets specially, so quoting `"fastapi[standard]"` is safer.

Run FastAPI in development:

```bash
uv run fastapi dev main.py
```

What it does:

- uses the backend project's environment;
- runs the `fastapi` command installed in `.venv`;
- starts the development server for `main.py`.

Why `uv run`: you usually do not need to manually activate the virtual environment with `source .venv/bin/activate`.

### What To Commit

Commit:

```text
backend/pyproject.toml
backend/uv.lock
```

Do not commit:

```text
backend/.venv/
__pycache__/
*.pyc
```

What to remember:

```text
uv = tool
pyproject.toml = declared dependencies/config
uv.lock = exact resolved dependency versions
.venv = installed local environment
uv run = run a command inside the managed environment
```

## Docker And Containers

Docker packages an app's runtime so it can run consistently outside the local machine setup. It does not replace knowing how the app runs; it makes that runtime explicit.

### Core Concepts And Commands

- Image: blueprint containing runtime, dependencies, app files, and startup command.
- Container: running or stopped instance of an image.
- Docker CLI: `docker` command you type.
- Docker engine: background service that builds images and runs containers.

Useful commands:

```bash
docker images          # local images
docker ps              # running containers
docker ps -a           # all containers, including stopped ones
docker stop <id/name>  # stop a running container
```

Built images live in Docker's local image store, not as normal project files. Use `docker images` to inspect them.

### Backend Dockerfile

Current backend Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

Key lines:

- `FROM python:3.11-slim`: start from a Python 3.11 image. `slim` is smaller than the full image but may need extra OS packages for some dependencies later.
- `WORKDIR /app`: set `/app` as the working directory inside the image.
- `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/`: copy the `uv` binaries from the official `uv` image into this image.
- `COPY pyproject.toml uv.lock ./`: copy dependency metadata before app code so Docker can cache dependency installation.
- `RUN uv sync --frozen --no-dev`: install dependencies from `uv.lock` without changing the lockfile and without dev-only dependencies.
- `COPY . .`: copy backend source files into `/app`.
- `EXPOSE 8000`: document that the containerized app listens on port `8000`; it does not publish the port by itself.
- `CMD [...]`: default command when the container starts.

### Build Context And .dockerignore

In:

```bash
docker build -t todo-backend .
```

`.` is the build context: the directory Docker can copy files from. Build from `backend/` because the Dockerfile, `pyproject.toml`, `uv.lock`, `main.py`, and `todo.py` are there.

`.dockerignore` keeps machine-local/generated files out of the build context:

```text
.venv/
__pycache__/
*.py[cod]
```

This matters because the local `.venv` is machine-specific and can be large; the image should install its own dependencies with `uv sync`.

### Ports, EXPOSE, And Port Mapping

A port is a numbered communication door. In `http://127.0.0.1:8001/docs`, `127.0.0.1` is your machine and `8001` is the host port.

Containers have their own network space, so Docker maps host ports to container ports:

```bash
docker run -p 8001:8000 todo-backend
```

Format:

```text
-p HOST_PORT:CONTAINER_PORT
```

Meaning:

```text
host port 8001 -> container port 8000
```

`EXPOSE 8000` documents the intended container port. `docker run -p ...` performs the actual mapping.

If host port `8000` is already used, this error can appear:

```text
Bind for 0.0.0.0:8000 failed: port is already allocated
```

Fix: use a free host port, such as `8001`, or stop the process/container using `8000`.

Useful checks:

```bash
docker ps
lsof -i :8000
```

### CMD Exec Form Vs Shell Form

Exec form:

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

Shell form:

```dockerfile
CMD uv run fastapi run main.py --host 0.0.0.0 --port 8000
```

Exec form starts the program directly and passes each list item as one argument. Shell form runs through `/bin/sh -c`, which is useful only when shell features like `&&`, pipes, or variable expansion are needed.

Use exec form for normal app startup because signal handling and argument passing are cleaner.

`--host 0.0.0.0` matters in containers: `127.0.0.1` would mean "inside the container only," while `0.0.0.0` listens on interfaces Docker can forward to.

### Build And Run Flow

From `backend/`:

```bash
docker build -t todo-backend .
docker images todo-backend
docker run -p 8001:8000 todo-backend
```

`-t todo-backend` tags the image. Without an explicit tag, Docker uses `latest`, so `todo-backend` means `todo-backend:latest`.

Verify:

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/tasks
```

Foreground vs detached:

```bash
docker run -p 8001:8000 todo-backend      # foreground, logs in terminal, Ctrl+C stops
docker run -d -p 8001:8000 todo-backend   # detached/background
```

What to remember: image = blueprint; container = instance; `docker build` creates image; `docker run` creates/runs container; `-p` connects host networking to container networking.

## Project Organization And Git Hygiene

### Why Folder Structure Evolves

Small projects can start with a few files:

```text
backend/
  main.py
  todo.py
```

Larger projects split by responsibility:

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

The goal is not to create folders for appearance. The goal is to reduce confusion when responsibilities start mixing.

### Common Backend Folders

Common responsibilities:

- `domain/`: business concepts like `Task` and `TodoList`;
- `schemas/`: Pydantic request/response models;
- `api/` or `routes/`: FastAPI route functions;
- `repositories/`: data access logic;
- `db/`: database connection/session/table setup;
- `tests/`: automated tests.

Current decision: keep the backend simple until there is real pressure to split files.

### Generated Files And .gitignore

Some files are source files and should be committed. Others are generated locally and should be ignored.

Commit:

```text
.py source files
pyproject.toml
uv.lock
Dockerfile when created
.dockerignore when created
```

Ignore:

```text
.venv/
__pycache__/
*.pyc
```

Why this matters: commit files needed to reproduce the project, not machine-local output.

## Future Study Guide Structure

As the notes grow, `LEARNINGS.md` may become too large to review comfortably.

A future split could be:

```text
study-guide/
  README.md
  python-oop.md
  fastapi-http.md
  pydantic.md
  dependency-management-uv.md
  docker.md
  project-organization.md
```

Then `LEARNINGS.md` can become an index that links to topic-specific files.

Reason to split:

- easier review by topic;
- less scrolling;
- more room for detailed examples;
- fewer unrelated concepts in one file.

Do not split just for structure. Split when the file becomes hard to use as a study guide.

## Deferred Topics

These topics have been discussed or planned but not implemented deeply yet. Expand them only when the project reaches them.

- SQL Server persistence.
- React frontend.
- Frontend deployment with Vercel.
- Backend deployment target selection.
- Unit tests and API tests.
- CI/CD.
