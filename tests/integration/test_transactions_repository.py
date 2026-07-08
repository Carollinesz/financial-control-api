from datetime import date
from decimal import Decimal

from app.repositories import transactions as repo


def _debit(**kwargs):
    defaults = {
        "account_id": 1,
        "transaction_date": date(2024, 1, 15),
        "value": Decimal("-50.00"),
        "description": "Supermercado",
        "category": "Alimentação",
        "type": "debit",
        "tracking": True,
    }
    return repo.create(kwargs.pop("db"), {**defaults, **kwargs})


# ── Empty / basic ────────────────────────────────────────────────────────────

def test_list_all_empty_returns_empty_list(db):
    assert repo.list_all(db) == []


def test_list_all_returns_created(db):
    _debit(db=db, description="Padaria")
    _debit(db=db, description="Farmácia")
    result = repo.list_all(db)
    assert {t.description for t in result} == {"Padaria", "Farmácia"}


def test_list_all_orders_by_transaction_id_desc(db):
    first = _debit(db=db, description="Primeiro")
    second = _debit(db=db, description="Segundo")
    result = repo.list_all(db)
    assert [t.transaction_id for t in result] == [second.transaction_id, first.transaction_id]


# ── Filters ───────────────────────────────────────────────────────────────────

def test_list_all_filters_by_account_id(db):
    _debit(db=db, account_id=1, description="Conta 1")
    _debit(db=db, account_id=2, description="Conta 2")
    result = repo.list_all(db, account_id=1)
    assert [t.description for t in result] == ["Conta 1"]


def test_list_all_filters_by_type(db):
    _debit(db=db, type="debit", description="Débito")
    _debit(
        db=db,
        type="credit",
        description="Crédito",
        details={"installments": 2, "first_payment": "2024-02-01"},
    )
    result = repo.list_all(db, type="credit")
    assert [t.description for t in result] == ["Crédito"]


def test_list_all_filters_by_category_case_insensitive_partial_match(db):
    _debit(db=db, category="Alimentação", description="Mercado")
    _debit(db=db, category="Transporte", description="Uber")
    result = repo.list_all(db, category="aliment")
    assert [t.description for t in result] == ["Mercado"]


def test_list_all_filters_by_tracking(db):
    _debit(db=db, tracking=True, description="Rastreado")
    _debit(db=db, tracking=False, description="Não rastreado")
    result = repo.list_all(db, tracking=False)
    assert [t.description for t in result] == ["Não rastreado"]


def test_list_all_filters_by_date_from(db):
    _debit(db=db, transaction_date=date(2024, 1, 10), description="Antigo")
    _debit(db=db, transaction_date=date(2024, 1, 20), description="Recente")
    result = repo.list_all(db, date_from=date(2024, 1, 15))
    assert [t.description for t in result] == ["Recente"]


def test_list_all_filters_by_date_to(db):
    _debit(db=db, transaction_date=date(2024, 1, 10), description="Antigo")
    _debit(db=db, transaction_date=date(2024, 1, 20), description="Recente")
    result = repo.list_all(db, date_to=date(2024, 1, 15))
    assert [t.description for t in result] == ["Antigo"]


def test_list_all_filters_by_date_range(db):
    _debit(db=db, transaction_date=date(2024, 1, 1), description="Fora do intervalo (antes)")
    _debit(db=db, transaction_date=date(2024, 1, 15), description="Dentro do intervalo")
    _debit(db=db, transaction_date=date(2024, 1, 31), description="Fora do intervalo (depois)")
    result = repo.list_all(db, date_from=date(2024, 1, 10), date_to=date(2024, 1, 20))
    assert [t.description for t in result] == ["Dentro do intervalo"]


def test_list_all_combines_multiple_filters(db):
    _debit(db=db, account_id=1, type="debit", description="Match")
    _debit(db=db, account_id=2, type="debit", description="Conta errada")
    _debit(
        db=db,
        account_id=1,
        type="credit",
        description="Tipo errado",
        details={"installments": 1, "first_payment": "2024-02-01"},
    )
    result = repo.list_all(db, account_id=1, type="debit")
    assert [t.description for t in result] == ["Match"]


# ── Pagination ────────────────────────────────────────────────────────────────

def test_list_all_respects_limit(db):
    for i in range(5):
        _debit(db=db, description=f"Item {i}")
    result = repo.list_all(db, limit=2)
    assert len(result) == 2


def test_list_all_respects_skip(db):
    created = [_debit(db=db, description=f"Item {i}") for i in range(3)]
    all_results = repo.list_all(db)
    skipped = repo.list_all(db, skip=1)
    assert skipped == all_results[1:]
    assert len(skipped) == 2
