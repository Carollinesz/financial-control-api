from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import account_balances as repo


def handle_list(db: Session) -> list:
    return repo.list_all(db)


def handle_get(db: Session, account_id: int):
    row = repo.get_by_account_id(db, account_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found",
        )
    return row
