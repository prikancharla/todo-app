# Dependency Management With uv

## The Problem uv Solves

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

## How uv, pyproject.toml, uv.lock, And .venv Fit Together

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

## Why The Files Are Inside backend/

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

## pyproject.toml

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

## What TOML Is

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

## uv.lock

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

## .venv

`.venv/` is the actual virtual environment folder.

It contains installed packages and Python environment files.

Do not commit it because:

- it is machine-specific;
- it can be recreated from `pyproject.toml` and `uv.lock`;
- it can be large;
- it may differ across operating systems and CPU architectures.

## Commands We Used

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

## What To Commit

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

