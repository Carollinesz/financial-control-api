from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import BankAccountBalanceRead
from app.services import account_balances as service

router = APIRouter(prefix="/account-balances", tags=["account-balances"])


@router.get("", response_model=list[BankAccountBalanceRead])
def handle_list_account_balances(db: Session = Depends(get_db)):
    return service.handle_list(db)


@router.get("/{account_id}", response_model=BankAccountBalanceRead)
def handle_get_account_balance(account_id: int, db: Session = Depends(get_db)):
    return service.handle_get(db, account_id)
