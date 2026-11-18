from fastapi import FastAPI, HTTPException, status
from taskcreate import TaskCreate, Task

app = FastAPI()

TASKS = [
    {"id": 1, "title": "Купить хлеб", "done": False},
    {"id": 2, "title": "Позвонить врачу", "done": False},
    {"id": 3, "title": "Закончить курс", "done": False},
]


@app.get("/tasks", response_model=list[Task])
def get_tasks(done: bool | None = None, limit: int = 10):
    if done is None:
        result = TASKS
    else:
        result = [task for task in TASKS if task["done"] == done]
    return result[:limit]

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    new_id = max((task["id"] for task in TASKS), default=0) + 1
    new_task = {"id": new_id, "title": payload.title, "done": payload.done}
    TASKS.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")