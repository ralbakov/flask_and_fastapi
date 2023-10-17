'''
Задание
Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. 
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StrictInt, StrictStr
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: StrictInt
    title: StrictStr
    description: StrictStr
    status: Optional[bool]

tasks = []

@app.get('/tasks', response_model=List[Task]) # возращает список всех задач
async def read_tasks():
    return tasks

@app.post('/tasks', response_model=Task)
async def add_task(task: Task):
    old_id = tasks[-1].id if tasks else 0  
    task.id = old_id + 1
    tasks.append(task)
    return task

@app.get('/tasks/{task_id}', response_model=Task)
async def load_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, v in enumerate(tasks):
        if task_id == v.id:
            tasks[i] = task
            return task
    raise HTTPException(status_code=404, detail="task not found")

@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    for i, v in enumerate(tasks):
        if v.id == task_id:
            del tasks[i]
            return tasks
    raise HTTPException(status_code=404, detail="task not found")


@app.get('/add_tasks')
async def add_tasks():
    for i in range(10):
        tasks.append(Task(id=i, title=f'task#{i}', description=f'description_{i}', status=True))
    return tasks