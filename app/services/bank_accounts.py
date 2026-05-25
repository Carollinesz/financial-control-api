from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import bank_account
from app.repositories import bank_accounts as repo
from app.schemas.schemas import BankAccountCreate, BankAccountUpdate


def handle_get(db: Session, account_id: int) -> bank_account:
    obj = repo.get_by_id(db, account_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found",
        )
    return obj


def handle_list(db: Session, skip: int, limit: int) -> list[bank_account]:
    return repo.list_all(db, skip=skip, limit=limit)


def handle_create(db: Session, payload: BankAccountCreate) -> bank_account:
    if repo.get_by_name(db, payload.bank_name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bank account '{payload.bank_name}' already exists",
        )
    return repo.create(db, payload.model_dump())


def handle_update(
    db: Session, account_id: int, payload: BankAccountUpdate
) -> bank_account:
    obj = handle_get(db, account_id)
    data = payload.model_dump(exclude_unset=True)
    if "bank_name" in data and data["bank_name"] != obj.bank_name:
        if repo.get_by_name(db, data["bank_name"]) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bank account '{data['bank_name']}' already exists",
            )
    return repo.update(db, obj, data)


def handle_delete(db: Session, account_id: int) -> None:
    obj = handle_get(db, account_id)
    repo.delete(db, obj)
