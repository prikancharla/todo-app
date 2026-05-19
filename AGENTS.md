# AGENTS.md

## Project Learning Journal

This repo is a hands-on learning project for software engineering fundamentals through a todo app.

The assistant must maintain `LEARNINGS.md` as a beginner-friendly study guide. Its purpose is to help the user return days or weeks later, understand what was learned, remember why decisions were made, and continue the project without rereading the entire chat.

`LEARNINGS.md` is not a changelog and not an exhaustive action log.

## Quality Standard For LEARNINGS.md

Before adding or changing a note, ask:

- Would this help a beginner reconstruct the concept later?
- Did the user actually encounter, ask about, debug, or decide this?
- Is the idea transferable beyond this exact line of code?
- Does it explain the mental model, not just the final answer?
- Would a command, code snippet, or concrete example make it easier to remember?

Prefer notes that explain:

- What the concept/tool is.
- Why it was needed.
- How it appears in this project.
- What commands or syntax matter.
- What files are read, written, generated, or committed.
- What mistake, confusion, or tradeoff came up.
- What the user should remember next time.

For implementation walkthroughs, especially Dockerfiles, config files, CLI workflows, API routes, database setup, and deployment setup, preserve the line-by-line reasoning at a beginner level. Do not only record the final file. Explain each important line or command as an example of a broader concept.

Use this order when possible:

1. General concept.
2. Why it matters.
3. How it applies in this project.
4. Concrete command or file line.
5. Common confusion or gotcha.
6. What to remember.

Avoid notes that:

- Merely record that a file, helper, function, or route was added.
- Are narrow implementation trivia without a transferable lesson.
- Are abstract one-line definitions with no beginner context.
- Over-prioritize headings/structure over explanation.
- Add future topics before the project actually reaches them.
- Repeat an existing section without deepening it.

## Command Documentation Standard

When documenting a command in `LEARNINGS.md`, explain:

- Where to run it from.
- What the command does.
- What files or state it reads.
- What files or state it writes/changes.
- Why important flags/options are used.
- What result to expect.
- Whether any generated files should be committed or ignored.

Example command-note quality:

```markdown
`uv add "fastapi[standard]"`

Run from `backend/`.

This adds FastAPI to the backend project. `uv` updates `pyproject.toml`, resolves exact dependency versions into `uv.lock`, and installs packages into `.venv/`.

The quotes protect the `[standard]` extra from shell interpretation.
```

## Tool And File Relationship Standard

When documenting a tool, explain how it relates to project files and runtime behavior.

Examples:

- For `uv`, explain the relationship between `uv`, `pyproject.toml`, `uv.lock`, `.venv/`, and `uv run`.
- For FastAPI, explain how `app`, route decorators, path parameters, request bodies, response models, and `/docs` relate.
- For Pydantic, explain request models vs response models vs domain classes.
- For Docker, explain Dockerfile, image, container, build context, port mapping, and ignored files.

## Topics To Capture Deeply

Prioritize deeper notes for concepts the user has actively encountered:

- Python classes, objects, constructors, `self`, attributes, methods, and imports.
- Getters, setters, Python properties, backing fields, validation, and encapsulation.
- Decorators such as `@dataclass`, `@property`, `@app.get`, and `@app.post`.
- Dataclasses and when they are useful or limiting.
- Type hints, runtime validation, optional values, defaults, positional arguments, and keyword arguments.
- Data structures such as lists and dictionaries when they affect design.
- FastAPI routes, HTTP methods, path/query parameters, request bodies, response serialization, status codes, and automatic docs.
- Pydantic models, validation, request vs response schemas, defaults, optional fields, and model-to-dict conversion.
- Dependency management with `uv`, `pyproject.toml`, `uv.lock`, virtual environments, and `uv run`.
- Docker concepts as they are implemented, not before.
- Git/repo hygiene such as `.gitignore`, lockfiles, generated files, and what to commit.

## LEARNINGS.md Structure

Use larger topic sections with detailed subsections:

```markdown
# Learnings

## Project Snapshot

Current architecture, tools, files, routes, and known limitations.

## Topic Area

### Specific Concept

Explain the concept clearly enough for a beginner to review later.

Include examples, commands, and common mistakes when useful.
```

Good larger sections include:

- How To Use This File
- Project Snapshot
- Python Fundamentals And OOP
- Backend Domain Design
- FastAPI And HTTP APIs
- Pydantic And Validation
- Dependency Management With uv
- Docker And Containers
- Project Organization And Git Hygiene
- Deferred Topics

Prefer concept-based organization over strict chronology. The file should read like a practical study guide, not a transcript.

## Maintenance Rules

When the user asks for review, feedback, moves to a new concept, expresses confusion, or receives an explanation that meets the quality bar, proactively update `LEARNINGS.md` without waiting for a separate reminder.

If a topic already exists, improve the existing section rather than duplicating it.

If the user says the notes are too shallow, review the relevant section for mental model, commands, file relationships, examples, and common mistakes.

If a topic has only been mentioned but not worked through, keep it in a short deferred section until it becomes active.

Do not use subagents to edit `LEARNINGS.md` unless the user explicitly approves the proposed note changes first.
