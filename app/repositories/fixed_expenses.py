from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import fixed_expense


def get_by_id(db: Session, expense_id: int) -> fixed_expense | None:
    return db.get(fixed_expense, expense_id)


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[fixed_expense]:
    stmt = select(fixed_expense).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())


def create(db: Session, data: dict) -> fixed_expense:
    obj = fixed_expense(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, obj: fixed_expense, data: dict) -> fixed_expense:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: fixed_expense) -> None:
    db.delete(obj)
    db.commit()
