# AGENTS.md

## Project Purpose

This repo is a hands-on learning project for software engineering fundamentals through a todo app.

Learning path:

1. Design Python OOP classes.
2. Build a FastAPI backend.
3. Integrate SQL Server persistence.
4. Build a simple React frontend.
5. Deploy the FastAPI backend.
6. Deploy the frontend.
7. Later: CI/CD.
8. Later: add an assistant service that can perform todo add/edit operations.

Current stage: the FastAPI backend exists and has been packaged with a Dockerfile. The next major step is choosing and using a backend deployment service.

## Learning Journal

Maintain `LEARNINGS.md` and the `study-guide/` folder as a beginner-friendly study guide.

`LEARNINGS.md` is the index and current project snapshot. Detailed concept notes live in topic files under `study-guide/`.

The guide should help the user return days or weeks later and understand:

- what was learned;
- why design choices were made;
- how concepts appear in this project;
- what commands, files, and runtime behavior matter;
- what mistakes, confusions, or tradeoffs came up.

It is not a changelog, transcript, or exhaustive action log.

## When To Update The Study Guide

Update the study guide when the user asks for review or feedback, moves into a new concept, expresses confusion, debugs an issue, makes a meaningful design/tooling decision, or receives an explanation that would be useful to revisit later.

If a topic already exists, improve that topic file instead of creating a duplicate. If a topic has only been mentioned but not worked through, keep it short in `study-guide/deferred-topics.md`.

Keep `LEARNINGS.md` focused on navigation and the current project snapshot. Do not use subagents to edit study-guide files unless the user explicitly approves the proposed note changes first.

## Quality Bar For Notes

Before adding or changing a note, check that it:

- helps a beginner reconstruct the mental model later;
- is based on something the user actually encountered, asked about, debugged, or decided;
- is transferable beyond one exact line of code;
- explains why the idea matters in this project;
- includes a concrete command, code snippet, or file example when that would make the idea easier to remember.

Prefer concept-based organization over strict chronology. Avoid notes that only say a file/function/route was added.

## Command And Tool Notes

When documenting a command in the study guide, explain:

- where to run it from;
- what the command does;
- what files or state it reads;
- what files or state it writes or changes;
- why important flags/options are used;
- what result to expect;
- whether generated files should be committed or ignored.

When documenting a tool, explain how it relates to project files and runtime behavior. Important relationships for this project:

- `uv`, `pyproject.toml`, `uv.lock`, `.venv/`, and `uv run`.
- FastAPI `app`, route decorators, request bodies, response models, status codes, and `/docs`.
- Pydantic request models, response models, defaults, validation, and model-to-dict conversion.
- Dockerfile, build context, image, container, port mapping, `.dockerignore`, and generated files.
- Git working tree, staging area, commits, branches, lockfiles, ignored files, and what to commit.

## Topics To Capture Deeply

Prioritize deeper beginner notes for concepts the user actively encounters:

- Python classes, objects, constructors, `self`, attributes, methods, imports, and properties.
- Type hints, runtime validation, optional values, defaults, positional arguments, and keyword arguments.
- Lists and dictionaries when they affect design.
- FastAPI routes, HTTP methods, path/query parameters, request bodies, serialization, and errors.
- Pydantic schemas and validation.
- Dependency management with `uv`.
- Docker concepts as implemented in this project.
- SQL Server and database persistence when implemented.
- React/frontend concepts when implemented.
- Deployment concepts when implemented.
