from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import TransactionCreate, TransactionRead, TransactionUpdate
from app.services import transactions as service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
def handle_list_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.handle_list(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=TransactionRead)
def handle_get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return service.handle_get(db, transaction_id)


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def handle_create_transaction(
    payload: TransactionCreate, db: Session = Depends(get_db)
):
    try:
        return service.handle_create(db, payload)
    except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error)
            )


@router.patch("/{transaction_id}", response_model=TransactionRead)
def handle_update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
):
    return service.handle_update(db, transaction_id, payload)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def handle_delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    service.handle_delete(db, transaction_id)
