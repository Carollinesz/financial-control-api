from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import TransactionCreate, TransactionRead, TransactionUpdate, TransactionUploadResult
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


@router.post("/upload", response_model=TransactionUploadResult, status_code=status.HTTP_200_OK)
async def handle_upload_transactions(
    account_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = file.filename or ""
    if not (filename.endswith(".xlsx") or filename.endswith(".xls")):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only .xlsx and .xls files are supported",
        )
    contents = await file.read()
    return service.handle_upload_xlsx(db, account_id, contents, filename)
