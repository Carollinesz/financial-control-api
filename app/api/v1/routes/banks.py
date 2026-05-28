from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import BanksRead
from app.services import banks as service

router = APIRouter(prefix="/banks", tags=["banks"])


@router.get("", response_model=list[BanksRead])
def handle_list_bank_accounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.handle_list(db, skip=skip, limit=limit)


@router.get("/{bank_id}", response_model=BanksRead)
def handle_get_bank_account(bank_id: int, db: Session = Depends(get_db)):
    return service.handle_get(db, bank_id)

