import pandas as pd
from ofxparse import OfxParser

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.models import transaction
from app.schemas.schemas import TransactionCreate


def get_by_id(db: Session, transaction_id: int) -> transaction | None:
    obj = db.get(transaction, transaction_id)
    if obj is None or obj.type != "transaction":
        return None
    return obj


def list_all(db: Session, skip: int = 0, limit: int = 100) -> list[transaction]:
    stmt = (
        select(transaction)
        .where(transaction.type == "transaction")
        .offset(skip)
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def create(db: Session, data: dict) -> transaction:
    obj = transaction(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj




def update(db: Session, obj: transaction, data: dict) -> transaction:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: transaction) -> None:
    db.delete(obj)
    db.commit()


def bulk_create(db: Session, rows: list[dict]) -> list[transaction]:
    objs = [transaction(**row) for row in rows]
    db.add_all(objs)
    db.commit()
    for obj in objs:
        db.refresh(obj)
    return objs

