from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.elderly import ElderlySchema, ElderlyCreate
from models.elderly import Elderly
from utils.redis_cache import get_from_cache, set_in_cache, delete_from_cache

def add_elderly_service(elderly: ElderlyCreate, db: Session) -> ElderlySchema:
    existing_elderly = db.query(Elderly).filter(Elderly.id == elderly.id).first()
    if existing_elderly:
        raise HTTPException(status_code=400, detail="Elderly with this ID already exists")

    new_elderly = Elderly(id=elderly.id, name=elderly.name)
    db.add(new_elderly)
    db.commit()
    db.refresh(new_elderly)

    print("🧹 Clearing elderly list cache and specific elderly cache")
    delete_from_cache("elderly_list")
    delete_from_cache(f"elderly_{new_elderly.id}")

    return new_elderly

def get_all_elderly_service(db: Session) -> list[ElderlySchema]:
    cache_key = "elderly_list"

    cached_data = get_from_cache(cache_key)
    if cached_data:
        print("✅ Retrieved elderly list from Redis cache")
        return [ElderlySchema(**e) for e in cached_data]

    elderly = db.query(Elderly).all()
    result = [ElderlySchema.from_orm(e) for e in elderly]
    print("📦 Retrieved elderly list from DB and storing in Redis")
    set_in_cache(cache_key, [e.dict() for e in result], ttl=300)

    return result


def delete_elderly_service(elderly_id: int, db: Session) -> dict:
    elderly = db.query(Elderly).filter(Elderly.id == elderly_id).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="Elderly not found")

    db.delete(elderly)
    db.commit()

    delete_from_cache("elderly_list")
    delete_from_cache(f"elderly_{elderly_id}")

    return {"message": f"Elderly {elderly_id} deleted successfully"}
