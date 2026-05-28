from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import CreditInstallmentRead
from app.services import credit_installments as service

router = APIRouter(prefix="/credit-installments", tags=["credit-installments"])


@router.get("", response_model=list[CreditInstallmentRead])
def handle_list_credit_installments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.handle_list(db, skip=skip, limit=limit)


@router.get("/{transaction_id}", response_model=list[CreditInstallmentRead])
def handle_get_credit_installments(transaction_id: int, db: Session = Depends(get_db)):
    return service.handle_get_by_transaction(db, transaction_id)
