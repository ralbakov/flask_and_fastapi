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
   
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, StrictInt, StrictStr, StrictBool
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory='hw_les_05/templates')

class Task(BaseModel):
    id: StrictInt
    title: StrictStr
    description: StrictStr
    status: Optional[StrictBool]

tasks = []

@app.get('/',response_class=HTMLResponse) #главная страница
async def homepage(request: Request):
    return templates.TemplateResponse('base.html', 
                                      context={'request': request, 
                                               'title': 'Start page', 
                                               'content': "Добро пожаловать на главную страницу"})

@app.get('/tasks/', response_model=List[Task]) # возращает список всех задач
async def read_tasks(request: Request):
    return templates.TemplateResponse('tasks.html', 
                                      context={'request': request, 
                                               'title': 'Tasks', 
                                               'content': tasks
                                               })

@app.post('/tasks/', response_model=Task) # добавляет задачи
async def add_task(request: Request, title: str = Form(), description: str = Form(), status: bool = Form()):
    if tasks:
        id = tasks[-1].id + 1
    else:
        id = 1
    task = Task(id=id, title=title, description=description, status=status)
    tasks.append(task)
    return templates.TemplateResponse('tasks.html', 
                                            context={'request': request, 
                                                    'title': 'Tasks', 
                                                    'content': tasks
                                                    })

@app.get('/tasks/{task_id}', response_class=HTMLResponse) # возвращает задачу с указанным идентификатором
async def load_task(request: Request, task_id: int):
    for task in tasks:
        if task.id == task_id:
            return templates.TemplateResponse('task_id.html', 
                                      context={'request': request, 
                                               'title': f'Tasks {task_id}', 
                                               'content': task
                                               })
    raise HTTPException(status_code=404, detail="Task not found")

@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(request: Request, task_id: int, title: str = Form(), description: str = Form(), status: bool = Form()):
    print(task_id)
    for i, task_ in enumerate(tasks):
        if task_.id == task_id:
            task = Task(id=task_id, title=title, description=description, status=status)
            tasks[i] = task
            return templates.TemplateResponse('task_id.html', 
                                        context={'request': request, 
                                                'title': f'Tasks {task_id}', 
                                                'content': task
                                                })
    raise HTTPException(status_code=404, detail="task not found")

# @app.delete('/tasks/{task_id}', response_class=HTMLResponse)
# async def del_task(request: Request, task_id: int):
#     for i, v in enumerate(tasks):
#         if v.id == task_id:
#             del tasks[i]
#             return templates.TemplateResponse('tasks.html', 
#                                             context={'request': request, 
#                                                     'title': 'Tasks', 
#                                                     'content': tasks
#                                                     })
#     raise HTTPException(status_code=404, detail="task not found")