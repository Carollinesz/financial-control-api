from sqlalchemy import text
from sqlalchemy.orm import Session


def list_all(db: Session) -> list:
    result = db.execute(
        text("SELECT * FROM bank_account_balance_view ORDER BY account_id")
    )
    return result.mappings().all()


def get_by_account_id(db: Session, account_id: int):
    result = db.execute(
        text("SELECT * FROM bank_account_balance_view WHERE account_id = :account_id"),
        {"account_id": account_id},
    )
    return result.mappings().first()
