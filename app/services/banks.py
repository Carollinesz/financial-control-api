from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import banks
from app.repositories import banks as repo


def handle_get(db: Session, bank_id: int) -> banks:
    obj = repo.get_by_id(db, bank_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {bank_id} not found",
        )
    return obj


def handle_list(db: Session, skip: int, limit: int) -> list[banks]:
    return repo.list_all(db, skip=skip, limit=limit)
