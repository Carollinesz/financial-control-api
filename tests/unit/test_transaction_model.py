import pytest
from datetime import date
from decimal import Decimal

from app.models.models import transaction


def _debit(**kwargs):
    defaults = {
        "transaction_date": date(2024, 1, 15),
        "value": Decimal("-50.00"),
        "description": "Supermercado",
        "type": "debit",
    }
    return transaction(**{**defaults, **kwargs})


def _credit(**kwargs):
    defaults = {
        "transaction_date": date(2024, 1, 15),
        "value": Decimal("-1200.00"),
        "description": "Notebook",
        "type": "credit",
        "details": {
            "installments": 3,
            "first_payment": "2024-02-01",
            "interest": 0.0,
        },
    }
    return transaction(**{**defaults, **kwargs})


# ── Debit ─────────────────────────────────────────────────────────────────────

def test_debit_valid():
    t = _debit()
    assert t.type == "debit"
    assert t.description == "Supermercado"


def test_debit_default_tracking_true():
    t = _debit()
    assert t.tracking is True


def test_debit_default_category():
    t = _debit()
    assert t.category == "Outros"


# ── Credit ────────────────────────────────────────────────────────────────────

def test_credit_valid():
    t = _credit()
    assert t.type == "credit"
    assert t.details["installments"] == 3


def test_credit_defaults_installments_to_1_when_missing():
    t = _credit(details={"first_payment": "2024-02-01"})
    assert t.details["installments"] == 1


def test_credit_defaults_interest_to_zero_when_missing():
    t = _credit(details={"installments": 2, "first_payment": "2024-02-01"})
    assert t.details["interest"] == 0.0


def test_credit_without_details_raises():
    with pytest.raises(ValueError, match="details"):
        transaction(
            transaction_date=date(2024, 1, 15),
            value=Decimal("-500.00"),
            description="Compra",
            type="credit",
        )


def test_credit_with_none_details_raises():
    with pytest.raises(ValueError, match="details"):
        transaction(
            transaction_date=date(2024, 1, 15),
            value=Decimal("-500.00"),
            description="Compra",
            type="credit",
            details=None,
        )


def test_credit_without_first_payment_raises():
    with pytest.raises(ValueError, match="first_payment"):
        _credit(details={"installments": 2})


def test_credit_installments_zero_raises():
    with pytest.raises(ValueError, match="installments"):
        _credit(details={"installments": 0, "first_payment": "2024-02-01"})


def test_credit_installments_above_99_raises():
    with pytest.raises(ValueError, match="installments"):
        _credit(details={"installments": 100, "first_payment": "2024-02-01"})


def test_credit_installments_boundary_1_valid():
    t = _credit(details={"installments": 1, "first_payment": "2024-02-01"})
    assert t.details["installments"] == 1


def test_credit_installments_boundary_99_valid():
    t = _credit(details={"installments": 99, "first_payment": "2024-02-01"})
    assert t.details["installments"] == 99


def test_credit_invalid_first_payment_string_raises():
    with pytest.raises(ValueError):
        _credit(details={"installments": 2, "first_payment": "not-a-date"})


def test_credit_first_payment_as_date_object_valid():
    t = _credit(details={"installments": 2, "first_payment": date(2024, 2, 1)})
    assert t.details["first_payment"] == date(2024, 2, 1)
