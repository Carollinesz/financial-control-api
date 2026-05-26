import io
from decimal import Decimal, InvalidOperation

import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.models.models import transaction
from app.repositories import bank_accounts as bank_accounts_repo
from app.repositories import transactions as repo
from app.schemas.schemas import TransactionCreate, TransactionUpdate, TransactionUploadResult, UploadRowError



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


_REQUIRED_COLUMNS = {"transaction_date", "value", "description"}


def handle_upload_xlsx(db: Session, account_id: int, file_bytes: bytes, filename: str) -> TransactionUploadResult:
    _ensure_account_exists(db, account_id)

    engine = "openpyxl" if filename.endswith(".xlsx") else "xlrd"
    try:
        df = pd.read_excel(io.BytesIO(file_bytes), engine=engine)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not read file: {exc}")

    missing = _REQUIRED_COLUMNS - set(df.columns.str.strip().str.lower())
    if missing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing required columns: {', '.join(sorted(missing))}",
        )

    df.columns = df.columns.str.strip().str.lower()

    valid_rows: list[dict] = []
    errors: list[UploadRowError] = []

    for idx, row in df.iterrows():
        row_num = int(idx) + 2  # +2: 1-based + header row
        try:
            raw_date = row["transaction_date"]
            if pd.isna(raw_date):
                raise ValueError("transaction_date is required")
            if isinstance(raw_date, str):
                parsed_date = date.fromisoformat(raw_date.strip())
            else:
                parsed_date = pd.Timestamp(raw_date).date()

            raw_value = row["value"]
            if pd.isna(raw_value):
                raise ValueError("value is required")
            parsed_value = Decimal(str(raw_value)).quantize(Decimal("0.0001"))

            raw_desc = row["description"]
            if pd.isna(raw_desc) or str(raw_desc).strip() == "":
                raise ValueError("description is required")
            parsed_desc = str(raw_desc).strip()[:100]

            valid_rows.append({
                "account_id": account_id,
                "transaction_date": parsed_date,
                "value": parsed_value,
                "description": parsed_desc,
            })
        except (ValueError, InvalidOperation) as exc:
            errors.append(UploadRowError(row=row_num, error=str(exc)))

    if valid_rows:
        repo.bulk_create(db, valid_rows)

    return TransactionUploadResult(created=len(valid_rows), errors=errors)
