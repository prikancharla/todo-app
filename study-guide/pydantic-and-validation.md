# Pydantic And Validation

## What Pydantic Does

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

## Request Models

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

## Response Models

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

## `response_model`

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

## Optional Fields And Defaults In Pydantic

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

## Model To Dictionary Conversion

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

## Dictionary Unpacking With `**`

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

