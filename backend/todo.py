import uuid


class Task:

    def __init__(self, title: str, description: str = ""):
        self._uid = uuid.uuid4()
        self.title = title
        self.description = description
        self.is_complete = False

    def __repr__(self):
        return f"Task(title={self.title!r}, description={self.description!r}, uid={self.uid!r}, is_complete={self.is_complete!r})"

    @property
    def uid(self):
        return self._uid

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

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Description can only be None or a string")

        self._description = value

    @property
    def is_complete(self):
        return self._is_complete

    @is_complete.setter
    def is_complete(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_complete can only take True or False")

        self._is_complete = value

    def toggle_complete(self):
        self.is_complete = not self.is_complete

    def mark_complete(self):
        self.is_complete = True


class TodoList:

    def __init__(self):
        self.tasks: dict[uuid.UUID, Task] = {}

    def __repr__(self):
        return f"TodoList(Tasks={self.tasks!r})"

    def create_task(self, title, description=""):
        return self.add_task(Task(title, description))

    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("TodoList can only hold values of type Task")
        self.tasks[task.uid] = task
        return self.tasks[task.uid]

    def get_task(self, uid: uuid.UUID) -> Task:
        if not uid in self.tasks:
            raise KeyError(f"Task {uid} doesn't exist")
        return self.tasks[uid]

    def remove_task(self, uid):
        if not uid in self.tasks:
            raise KeyError(f"Task {uid} doesn't exist")
        del self.tasks[uid]

    def toggle_complete(self, uid):
        self.get_task(uid).toggle_complete()

    def list_tasks(self):
        return list(self.tasks.values())


def main():
    todolist = TodoList()
    todolist.create_task("write program")
    print(todolist.list_tasks())


if __name__ == "__main__":
    main()
