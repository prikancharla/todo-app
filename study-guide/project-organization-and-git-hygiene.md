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
.env.example when created
```

Ignore:

```text
.venv/
__pycache__/
*.pyc
.env and .env.* files
test, coverage, lint, and type-checking caches
Python build artifacts
```

Why this matters: commit files needed to reproduce the project, not machine-local output. A lockfile such as `uv.lock` is not generated clutter: it records the dependency versions needed for a repeatable install, so it belongs in Git.

`.gitignore` is a project-wide agreement about generated and secret-bearing files. Keep it focused on files this project creates or is likely to create. Personal editor preferences are usually better kept in each developer's global Git ignore file, rather than ignoring an entire editor folder that could later contain useful shared settings.

Ignoring a pattern only affects files that are not already tracked. If a secret was committed before adding it to `.gitignore`, remove it from Git tracking and rotate the secret; the ignore rule alone does not make the old commit safe.
