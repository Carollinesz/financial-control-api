from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.models.models import transaction
from app.repositories import bank_accounts as bank_accounts_repo
from app.repositories import transactions as repo
from app.schemas.schemas import TransactionCreate, TransactionUpdate



def _ensure_account_exists(db: Session, account_id: int) -> None:
    if bank_accounts_repo.get_by_id(db, account_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found",
        )


def handle_get(db: Session, transaction_id: int) -> transaction:
    obj = repo.get_by_id(db, transaction_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found",
        )
    return obj


def handle_list(db: Session, skip: int, limit: int) -> list[transaction]:
    return repo.list_all(db, skip=skip, limit=limit)


def handle_create(db: Session, payload: TransactionCreate) -> transaction:
    _ensure_account_exists(db, payload.account_id)
    return repo.create(db, payload.model_dump())


def handle_update(
    db: Session, transaction_id: int, payload: TransactionUpdate
) -> transaction:
    obj = handle_get(db, transaction_id)
    data = payload.model_dump(exclude_unset=True)
    if "account_id" in data:
        _ensure_account_exists(db, data["account_id"])
    return repo.update(db, obj, data)


def handle_delete(db: Session, transaction_id: int) -> None:
    obj = handle_get(db, transaction_id)
    repo.delete(db, obj)
