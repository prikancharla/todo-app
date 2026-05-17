# AGENTS.md

## Project Learning Journal

This repo is being used as a hands-on learning project for software engineering fundamentals through a todo app.

The assistant should continually maintain `LEARNINGS.md` as a concise but useful learning journal. The goal is not to document every action, but to preserve reusable concepts, tradeoffs, bugs, and design decisions the user encounters while building the project.

## Learning Update Instructions

Update `LEARNINGS.md` after meaningful learning moments, including:

- A new concept is introduced.
- A design choice is made.
- A bug reveals an important principle.
- A tool, framework, or library is added.
- The project structure changes.
- A deployment, environment, or dependency-management decision is made.

Do not update `LEARNINGS.md` for every tiny command or minor edit. Prefer high-signal notes the user can review later.

When updating the file:

- Preserve useful existing notes.
- Refine existing sections when a topic deepens instead of duplicating the topic.
- Keep explanations beginner-friendly but technically accurate.
- Capture the "why," not just the "what."
- Mention tradeoffs when multiple reasonable options exist.
- Use examples when they make syntax or behavior easier to remember.
- Omit shallow future-topic filler until the project actually reaches that topic.

## Learning Quality Bar

Before adding or changing a note in `LEARNINGS.md`, ask:

- Did the user actually encounter this concept or ask about it?
- Is this concept reusable later in the project?
- Does it explain a mistake, design decision, tradeoff, or tool behavior?
- Would a short example make the concept easier to remember?

Prioritize deeper notes for foundational concepts, including:

- Python classes, objects, constructors, `self`, attributes, and methods.
- Getters, setters, Python properties, backing fields, and encapsulation.
- Decorators such as `@dataclass`, `@property`, `@app.get`, and `@app.post`.
- Dataclasses and when they are useful or limiting.
- Type hints, runtime validation, optional values, defaults, positional arguments, and keyword arguments.
- Data structures such as lists and dictionaries, especially when they affect design.
- FastAPI routes, route decorators, path/query parameters, request bodies, response models, and automatic docs.
- Pydantic models, validation, request vs response schemas, defaults, optional fields, and model-to-dict conversion.
- Serialization and why internal Python objects are not the same as API responses.
- HTTP methods, status codes, and translating Python exceptions into HTTP errors.
- Dependency management with `uv`, `pyproject.toml`, `uv.lock`, and virtual environments.

Avoid long sections about topics only briefly discussed or not implemented yet, such as Docker, Vercel, CI/CD, databases, or frontend architecture. Mention them only in a short deferred section until the project reaches them.

## LEARNINGS.md Style

Use a readable topic-based structure:

```markdown
# Learnings

## Project Snapshot

Short summary of the current architecture and tools. Update only when the project shape changes meaningfully.

## Larger Topic Section

### Specific Concept

Explanation of the concept, with enough detail for later review.

Example when useful:

```python
...
```

Key lesson:
```

Prefer larger sections such as:

- Python And OOP
- Data Modeling And Design Decisions
- FastAPI And HTTP APIs
- Pydantic And Validation
- Dependency Management
- Current Design Decisions
- Deferred Topics

Not every topic needs the same format. Some concepts deserve longer explanations with examples; others only need a short note.

Prefer concept-based notes over strict chronological notes. The file should be easy to review by topic, not just by date.

## Maintenance Guidance

When the user asks for review, feedback, or moves to a new concept, consider whether `LEARNINGS.md` should be updated.

If the user points out a missing or shallow concept, review recent chat context and improve the relevant section, not just append a new note.

Merge overlapping topics when possible so `LEARNINGS.md` stays readable as a study guide.

Keep `LEARNINGS.md` concise enough to remain useful, but go deeper on concepts the user struggled with or explicitly asked to understand.
