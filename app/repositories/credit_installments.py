from sqlalchemy import text
from sqlalchemy.orm import Session


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list:
    result = db.execute(
        text("""
            SELECT * FROM credit_installments_view
            ORDER BY transaction_id, installment_number
            OFFSET :skip LIMIT :limit
        """),
        {"skip": skip, "limit": limit},
    )
    return result.mappings().all()


def get_by_transaction_id(db: Session, transaction_id: int) -> list:
    result = db.execute(
        text("""
            SELECT * FROM credit_installments_view
            WHERE transaction_id = :transaction_id
            ORDER BY installment_number
        """),
        {"transaction_id": transaction_id},
    )
    return result.mappings().all()
