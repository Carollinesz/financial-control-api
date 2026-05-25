from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.models import banks


def get_by_id(db: Session, bank_id: int) -> banks | None:
    return db.get(banks, bank_id)


def get_by_name(db: Session, bank_name: str) -> banks | None:
    stmt = select(banks).where(banks.bank_name == bank_name)
    return db.execute(stmt).scalar_one_or_none()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[banks]:
    stmt = select(banks).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, data: dict) -> banks:
    obj = banks(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, obj: banks, data: dict) -> banks:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: banks) -> None:
    db.delete(obj)
    db.commit()
