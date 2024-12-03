from fastapi import APIRouter, HTTPException
from models.elderly import Elderly

router = APIRouter()

elderly_list = {}

@router.post("/")
def add_elderly(name: str, id: int):
    if id in elderly_list:
        raise HTTPException(status_code=400, detail="Elderly person already exists")
    elderly_list[id] = Elderly(name, id)
    return {"message": f"Elderly person {name} added successfully"}

@router.get("/")
def get_elderly():
    return {"elderly": list(elderly_list.values())}

@router.post("/{id}/tasks")
def add_task_to_elderly(id: int, task: str):
    if id not in elderly_list:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    elderly_list[id].add_task(task)
    return {"message": f"Task '{task}' added for elderly {id}"}
