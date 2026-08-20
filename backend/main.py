from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from todo import TodoList
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["GET"],
)

todolist = TodoList()
todolist.create_task("buy milk")
todolist.create_task("set up internet")


class InputTaskData(BaseModel):
    title: str
    description: str = ""


class OutputTaskData(BaseModel):
    uid: str
    title: str
    description: str
    is_complete: bool


@app.get("/tasks", response_model=List[OutputTaskData])
def list_tasks():
    tasks = todolist.list_tasks()

    result = []

    for task in tasks:
        result.append(task_to_response(task))

    return result


@app.post("/tasks", response_model=OutputTaskData)
def create_task(input_task: InputTaskData):
    return task_to_response(todolist.create_task(**input_task.dict()))


def task_to_response(task):
    return {
        "uid": str(task.uid),
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete,
    }


@app.delete("/tasks/{uid}")
def remove_task(uid: uuid.UUID):
    try:
        todolist.remove_task(uid)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"delete": True, "uid": str(uid)}


@app.get("/tasks/{uid}", response_model=OutputTaskData)
def get_task(uid: uuid.UUID):
    try:
        task = todolist.get_task(uid)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_to_response(task)


@app.patch("/tasks/{uid}/toggle", response_model=OutputTaskData)
def toggle_complete(uid: uuid.UUID):
    try:
        todolist.toggle_complete(uid)
        task = todolist.get_task(uid)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_to_response(task)
