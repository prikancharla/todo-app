# Todo App

A hands-on learning project for software engineering fundamentals. The current application is a small FastAPI backend for managing todo tasks.

## Current Status

- FastAPI backend with an in-memory todo list.
- Docker packaging for the backend.
- No database or frontend yet.

Because task data is stored in memory, it is reset whenever the application restarts.

## Live API

The backend is deployed on Render:

- Interactive API documentation: <https://todo-app-7180.onrender.com/docs>
- Task list: <https://todo-app-7180.onrender.com/tasks>

The base URL does not have a route, so use one of the paths above rather than visiting only the service address.

## Prerequisites

To run the backend directly, install:

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)

Docker is optional, for running the containerized version.

## Run Locally

Clone the repository, then start the backend from the `backend/` directory:

```bash
git clone https://github.com/prikancharla/todo-app.git
cd todo-app/backend
uv run fastapi dev main.py
```

`uv` reads `pyproject.toml` and `uv.lock`, creates or reuses the local virtual environment, and runs FastAPI with the project's dependencies.

When the server starts, open:

- Interactive API documentation: <http://127.0.0.1:8000/docs>
- Task list: <http://127.0.0.1:8000/tasks>

Stop the server with `Ctrl+C`.

## Run With Docker

From the `backend/` directory, build the image and run a container:

```bash
docker build -t todo-backend .
docker run --rm -p 8001:8000 todo-backend
```

Then open:

- Interactive API documentation: <http://127.0.0.1:8001/docs>
- Task list: <http://127.0.0.1:8001/tasks>

The port mapping means your computer's port `8001` forwards to port `8000` inside the container. `--rm` removes the stopped container automatically.

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/tasks` | List all tasks. |
| `POST` | `/tasks` | Create a task. |
| `GET` | `/tasks/{uid}` | Get one task by its UUID. |
| `DELETE` | `/tasks/{uid}` | Delete a task by its UUID. |
| `PATCH` | `/tasks/{uid}/toggle` | Toggle a task's completion state. |

To create a task, send JSON like:

```json
{
  "title": "Buy milk",
  "description": "From the grocery store"
}
```

FastAPI's `/docs` page provides a browser interface for trying each endpoint.

## Project Layout

```text
backend/
  main.py        FastAPI routes and request/response models
  todo.py        Task and TodoList domain classes
  pyproject.toml Python project configuration and dependencies
  uv.lock        Locked dependency versions
  Dockerfile     Container build instructions
study-guide/     Beginner-friendly notes about the concepts used here
```
