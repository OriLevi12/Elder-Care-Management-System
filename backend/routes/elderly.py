from fastapi import APIRouter, HTTPException
from models.elderly import Elderly
from models.task import Task
from typing import Dict

router = APIRouter()

elderly_list: Dict[int, Elderly] = {}

@router.post("/")
def add_elderly(name: str, id: int):
    if id in elderly_list:
        raise HTTPException(status_code=400, detail="Elderly person already exists")
    elderly = Elderly(id=id, name=name)
    elderly_list[id] = elderly
    return {"message": f"Elderly person {name} added successfully"}

@router.get("/")
def get_elderly():
    return {"elderly": list(elderly_list.values())}

@router.delete("/{id}")
def delete_elderly(id: int):
    if id not in elderly_list:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    deleted = elderly_list.pop(id)
    return {"message": f"Elderly person {deleted.name} deleted successfully"}

@router.post("/{id}/tasks")
def add_task_to_elderly(id: int, description: str):
    if id not in elderly_list:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    try:
        task = Task(description=description)
        elderly_list[id].add_task(task)
        return {"message": f"Task '{description}' added for elderly {id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}/tasks")
def delete_task_from_elderly(id: int, description: str):
    if id not in elderly_list:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    try:
        elderly_list[id].delete_task(description)
        return {"message": f"Task '{description}' deleted for elderly {id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{id}/tasks/status")
def update_task_status(id: int, description: str, status: str):
    if id not in elderly_list:
        raise HTTPException(status_code=404, detail="Elderly person not found")
    try:
        updated_task = elderly_list[id].update_task_status(description, status)
        return {"message": f"Task '{description}' status updated to '{status}'", "task": updated_task.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
