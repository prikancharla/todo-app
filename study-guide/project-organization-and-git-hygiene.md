# Project Organization And Git Hygiene

## Why Folder Structure Evolves

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

## Common Backend Folders

Common responsibilities:

- `domain/`: business concepts like `Task` and `TodoList`;
- `schemas/`: Pydantic request/response models;
- `api/` or `routes/`: FastAPI route functions;
- `repositories/`: data access logic;
- `db/`: database connection/session/table setup;
- `tests/`: automated tests.

Current decision: keep the backend simple until there is real pressure to split files.

## Generated Files And .gitignore

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
