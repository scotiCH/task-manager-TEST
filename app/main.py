from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4

from .models import Task, TaskCreate, TaskUpdate, Status

app = FastAPI(title="Task Manager API")

tasks: dict[UUID, Task] = {}

@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate) -> Task:
    task_id = uuid4()
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        status=Status.created
    )
    tasks[task_id] = new_task
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/tasks/", response_model=list[Task])
def get_tasks() -> list[Task]:
    return list(tasks.values())

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, update_data: TaskUpdate) -> Task:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    current_task = tasks[task_id]
    updated_fields = update_data.dict(exclude_unset=True)
    updated_task = current_task.copy(update=updated_fields)
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: UUID) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]