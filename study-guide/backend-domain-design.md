# Backend Domain Design

## `Task` And `TodoList` Responsibilities

Current design:

- `Task`: stores one task's data and validates fields.
- `TodoList`: stores multiple tasks and provides collection operations.

Examples:

- `Task.toggle_complete()` changes one task.
- `TodoList.get_task(uid)` finds one task from the collection.
- `TodoList.remove_task(uid)` removes one task from the collection.

Why this matters: classes should have focused responsibilities. If every class knows everything, the code becomes hard to change.

## ID Ownership

We discussed several possible owners for task IDs:

- caller provides IDs;
- `Task` creates its own ID;
- `TodoList` assigns IDs;
- a future database assigns IDs.

Current decision: `Task` creates its own UUID, and `TodoList` stores tasks by UUID.

Why UUIDs:

- globally unique;
- easy to generate without a database;
- useful for API URLs.

Tradeoff:

- UUIDs are harder to read than integers;
- SQL databases often use integer primary keys;
- future database integration may change ID ownership.

What to remember: only one layer should own ID generation at a time.

## Lists Vs Dictionaries

A list is simple:

```python
tasks = [task1, task2]
```

But finding a task by ID requires scanning the list.

A dictionary is better for direct lookup:

```python
tasks = {
    task.uid: task
}
```

Current design: `TodoList` stores tasks in a dictionary keyed by UUID.

Why this matters:

- `get_task(uid)` can look up directly by ID;
- `remove_task(uid)` can delete directly by ID;
- API routes naturally work with IDs.

## Returning Internal Storage

Returning the raw internal dictionary exposes implementation details:

```python
return self.tasks
```

Returning a list hides the storage choice:

```python
return list(self.tasks.values())
```

Why this matters: outside code should not depend on whether tasks are stored in a dictionary, list, or database.

