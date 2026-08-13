# Learnings

## How To Use This Guide

This file is the index and current snapshot for the todo app study guide. Detailed notes live in `study-guide/` and are organized by concept, not by date.

Use this guide to review:

- what each technology or concept means;
- why we used it;
- how it appears in this project;
- what commands matter;
- what files are important;
- what mistakes or tradeoffs came up.

The guide should not record every small code edit. It should preserve high-value concepts that are likely to matter again.

## Project Snapshot

The project is currently a small FastAPI backend for a todo app.

Current repo shape:

```text
todo-app/
  AGENTS.md
  LEARNINGS.md
  .gitignore
  backend/
    .dockerignore
    main.py
    todo.py
    pyproject.toml
    uv.lock
    Dockerfile
  frontend/
    index.html
  study-guide/
    python-fundamentals-and-oop.md
    backend-domain-design.md
    fastapi-and-http-apis.md
    pydantic-and-validation.md
    dependency-management-with-uv.md
    networking-clients-servers-and-ports.md
    docker-and-containers.md
    deployment-on-render.md
    project-organization-and-git-hygiene.md
    git-basics.md
    html-document-structure.md
    css-basics-and-selectors.md
    deferred-topics.md
```

Current backend:

- `backend/todo.py` contains plain Python domain classes: `Task` and `TodoList`.
- `backend/main.py` contains the FastAPI app, Pydantic request/response models, and API routes.
- Dependencies are managed with `uv`.
- `backend/Dockerfile` defines how to package the FastAPI backend into a Docker image.
- `backend/.dockerignore` keeps generated local files out of the Docker build context.
- The backend has been deployed on Render and verified through API routes.
- Data is stored in memory in one global `TodoList`, so data resets when the app restarts.
- `README.md` provides clone, local-run, and Docker-run instructions for new contributors.
- `frontend/index.html` and `frontend/styles.css` form a static, styled mockup whose task markup matches the backend task shape.

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
- No interactive frontend yet: the static mockup has no JavaScript or backend connection.
- Docker packaging exists through `backend/Dockerfile` and `backend/.dockerignore`.
- Backend deployment on Render works for the current in-memory API.
- All users would currently share the same in-memory todo list.

## Study Guide Topics

- [Python Fundamentals And OOP](study-guide/python-fundamentals-and-oop.md)
- [Backend Domain Design](study-guide/backend-domain-design.md)
- [FastAPI And HTTP APIs](study-guide/fastapi-and-http-apis.md)
- [Pydantic And Validation](study-guide/pydantic-and-validation.md)
- [Dependency Management With uv](study-guide/dependency-management-with-uv.md)
- [Networking, Clients, Servers, And Ports](study-guide/networking-clients-servers-and-ports.md)
- [Docker And Containers](study-guide/docker-and-containers.md)
- [Deployment On Render](study-guide/deployment-on-render.md)
- [Project Organization And Git Hygiene](study-guide/project-organization-and-git-hygiene.md)
- [Git Basics Used In This Project](study-guide/git-basics.md)
- [HTML Document Structure](study-guide/html-document-structure.md)
- [CSS Basics And Selectors](study-guide/css-basics-and-selectors.md)
- [Deferred Topics](study-guide/deferred-topics.md)

## Updating This Guide

Add new notes to the most relevant topic file in `study-guide/`. Keep `LEARNINGS.md` focused on navigation and the project snapshot.

If a deferred topic becomes active, move it from `study-guide/deferred-topics.md` into a focused topic file.
