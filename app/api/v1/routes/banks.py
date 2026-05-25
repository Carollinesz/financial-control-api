from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import BanksCreate, BanksRead, BanksUpdate
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


@router.post("", response_model=BanksRead, status_code=status.HTTP_201_CREATED)
def handle_create_bank_account(
    payload: BanksCreate, db: Session = Depends(get_db)
):
    return service.handle_create(db, payload)


@router.patch("/{bank_id}", response_model=BanksRead)
def handle_update_bank_account(
    bank_id: int,
    payload: BanksUpdate,
    db: Session = Depends(get_db),
):
    return service.handle_update(db, bank_id, payload)


@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def handle_delete_bank_account(bank_id: int, db: Session = Depends(get_db)):
    service.handle_delete(db, bank_id)
