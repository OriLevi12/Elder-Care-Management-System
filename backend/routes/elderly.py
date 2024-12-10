from fastapi import APIRouter, HTTPException
from models.elderly import Elderly

router = APIRouter()

@router.post("/")
def add_elderly(name: str, id: int):
    try:
        Elderly.add(name, id)
        return {"message": f"Elderly person {name} added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_elderly():
    return {"elderly": Elderly.get_all()}

@router.delete("/{id}")
def delete_elderly(id: int):
    try:
        deleted = Elderly.delete(id)
        return {"message": f"Elderly person {deleted.name} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{id}/tasks")
def add_task_to_elderly(id: int, task: str):
    try:
        elderly = Elderly.get(id)
        elderly.add_task(task)
        return {"message": f"Task '{task}' added for elderly {id}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}/tasks")
def delete_task_from_elderly(id: int, task: str):
    try:
        elderly = Elderly.get(id)
        elderly.delete_task(task)
        return {"message": f"Task '{task}' deleted for elderly {id}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.put("/{id}/tasks/status")
def update_task_status(id: int, description: str, status: str):
    try:
        elderly = Elderly.get(id)
        updated_task = elderly.update_task_status(description, status)
        return {"message": f"Task '{description}' status updated to '{status}'", "task": updated_task.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
