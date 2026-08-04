# Python Fundamentals And OOP

## Classes And Objects

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

## Constructors And `self`

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

## Attributes And Methods

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

## Getters, Setters, And Python Properties

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

## Backing Fields And Internal Attributes

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

## Setter Recursion Bug

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

## Encapsulation

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

## Dataclasses

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

## Decorators

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

## Type Hints Vs Runtime Validation

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

## Optional Types Vs Default Values

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

## Positional Vs Keyword Arguments

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

## `__repr__`, `__str__`, And Object Display

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

## Python Modules And Imports

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

## `if __name__ == "__main__"`

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

