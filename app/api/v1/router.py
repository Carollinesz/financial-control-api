from fastapi import APIRouter

from app.api.v1.routes import bank_accounts, transactions, banks

api_router = APIRouter()
api_router.include_router(bank_accounts.router)
api_router.include_router(banks.router)
api_router.include_router(transactions.router)
