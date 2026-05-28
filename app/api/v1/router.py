from fastapi import APIRouter

from app.api.v1.routes import account_balances, bank_accounts, banks, credit_installments, fixed_expenses, transactions

api_router = APIRouter()
api_router.include_router(bank_accounts.router)
api_router.include_router(banks.router)
api_router.include_router(transactions.router)
api_router.include_router(fixed_expenses.router)
api_router.include_router(credit_installments.router)
api_router.include_router(account_balances.router)
