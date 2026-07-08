from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.schemas import BankAccountCreate
from app.models.models import bank_account


def get_by_id(db: Session, account_id: int) -> bank_account | None:
    return db.get(bank_account, account_id)


def get_by_name(db: Session, account_name: str) -> bank_account | None:
    stmt = select(bank_account).where(bank_account.account_name == account_name)
    return db.execute(stmt).scalar_one_or_none()


def list_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    bank_id: int | None = None,
    account_name: str | None = None,
    account_type: str | None = None,
) -> list[bank_account]:
    stmt = select(bank_account)
    if bank_id is not None:
        stmt = stmt.where(bank_account.bank_id == bank_id)
    if account_name is not None:
        stmt = stmt.where(bank_account.account_name.ilike(f"%{account_name}%"))
    if account_type is not None:
        stmt = stmt.where(bank_account.account_type.ilike(f"%{account_type}%"))
    stmt = stmt.offset(skip).limit(limit)
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
