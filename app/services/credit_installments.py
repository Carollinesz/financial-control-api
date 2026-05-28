from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import credit_installments as repo
from app.repositories import transactions as transactions_repo


def handle_list(db: Session, skip: int, limit: int) -> list:
    return repo.list_all(db, skip=skip, limit=limit)


def handle_get_by_transaction(db: Session, transaction_id: int) -> list:
    transaction = transactions_repo.get_by_id(db, transaction_id)
    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction {transaction_id} not found",
        )
    if transaction.type != "credit":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction {transaction_id} is not a credit transaction",
        )
    return repo.get_by_transaction_id(db, transaction_id)
