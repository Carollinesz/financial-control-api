from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import banks
from app.repositories import banks as repo
from app.schemas.schemas import BanksCreate, BanksUpdate


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


def handle_create(db: Session, payload: BanksCreate) -> banks:
    if repo.get_by_name(db, payload.bank_name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bank account '{payload.bank_name}' already exists",
        )
    return repo.create(db, payload.model_dump())


def handle_update(
    db: Session, bank_id: int, payload: BanksUpdate
) -> banks:
    obj = handle_get(db, bank_id)
    data = payload.model_dump(exclude_unset=True)
    if "bank_name" in data and data["bank_name"] != obj.bank_name:
        if repo.get_by_name(db, data["bank_name"]) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bank account '{data['bank_name']}' already exists",
            )
    return repo.update(db, obj, data)


def handle_delete(db: Session, bank_id: int) -> None:
    obj = handle_get(db, bank_id)
    repo.delete(db, obj)
