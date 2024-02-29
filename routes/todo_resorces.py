from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from models.models import CreateToDoRequest, UpdateToDoRequest, ToDo
from db.db import create_todo, get_todo, update_todo, delete_todo, get_all_todo
from fastapi.requests import Request

todos = APIRouter(prefix="/todos")
templates = Jinja2Templates(directory="templates")


@todos.post("/", response_model=ToDo)
async def create(todo: CreateToDoRequest):
    res = await create_todo(todo)
    return res


@todos.get("/all")
async def get_all(request: Request):
    todos_list = await get_all_todo()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos_list})


@todos.get("/{todo_id}", response_model=ToDo)
async def read(todo_id: int):
    res = await get_todo(todo_id)
    return res


@todos.put("/{todo_id}", response_model=ToDo)
async def update(todo_id: int, todo: UpdateToDoRequest):
    res = await update_todo(todo_id, todo)
    return res


@todos.delete("/{todo_id}", response_model=dict)
async def delete(todo_id: int):
    await delete_todo(todo_id)
    return {"message": "Todo deleted successfully"}
