import pytest


from app.core.database import SessionLocal
from app.models.models import bank_account, fixed_expense, transaction


@pytest.fixture(autouse=True)
def clean_db():
    yield
    db = SessionLocal()
    try:
        db.query(transaction).delete(synchronize_session=False)
        db.query(fixed_expense).delete(synchronize_session=False)
        db.query(bank_account).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
