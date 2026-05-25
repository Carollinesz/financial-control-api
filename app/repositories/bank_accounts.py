from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.schemas import BankAccountCreate
from app.models.models import bank_account


def get_by_id(db: Session, account_id: int) -> bank_account | None:
    return db.get(bank_account, account_id)


def get_by_name(db: Session, bank_name: str) -> bank_account | None:
    stmt = select(bank_account).where(bank_account.bank_name == bank_name)
    return db.execute(stmt).scalar_one_or_none()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[bank_account]:
    stmt = select(bank_account).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, data: dict) -> bank_account:
    obj = bank_account(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, obj: bank_account, data: dict) -> bank_account:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: bank_account) -> None:
    db.delete(obj)
    db.commit()
