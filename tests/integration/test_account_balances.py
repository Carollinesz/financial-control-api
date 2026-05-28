import pytest

BASE = "/api/v1/account-balances"
ACCOUNTS_BASE = "/api/v1/bank-accounts"
TRANSACTIONS_BASE = "/api/v1/transactions"


def _first_bank_id(client):
    return client.get("/api/v1/banks").json()[0]["bank_id"]


def _make_account(client, start_value=1000.0, name="Test Account"):
    resp = client.post(ACCOUNTS_BASE, json={
        "bank_id": _first_bank_id(client),
        "account_name": name,
        "account_type": "checking",
        "start_value": start_value,
    })
    return resp.json()["account_id"]


def _add_transaction(client, account_id, value, description="Test"):
    return client.post(TRANSACTIONS_BASE, json={
        "account_id": account_id,
        "transaction_date": "2024-01-15",
        "value": value,
        "description": description,
        "type": "debit",
        "tracking": True,
    }).json()


# ── List ──────────────────────────────────────────────────────────────────────

def test_list_empty(client):
    resp = client.get(BASE)
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_returns_account(client):
    _make_account(client)
    resp = client.get(BASE)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_list_multiple_accounts(client):
    _make_account(client, name="Conta A")
    _make_account(client, name="Conta B")
    assert len(client.get(BASE).json()) == 2


# ── Get ───────────────────────────────────────────────────────────────────────

def test_get_balance_no_transactions(client):
    acc = _make_account(client, start_value=1000.0)
    resp = client.get(f"{BASE}/{acc}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["account_id"] == acc
    assert float(data["start_value"]) == 1000.0
    assert float(data["total_gains"]) == 0.0
    assert float(data["total_expenses"]) == 0.0
    assert float(data["current_balance"]) == 1000.0


def test_get_balance_with_income(client):
    acc = _make_account(client, start_value=0.0)
    _add_transaction(client, acc, 500.0, "Salário")
    data = client.get(f"{BASE}/{acc}").json()
    assert float(data["total_gains"]) == 500.0
    assert float(data["total_expenses"]) == 0.0
    assert float(data["current_balance"]) == pytest.approx(500.0)


def test_get_balance_with_expense(client):
    acc = _make_account(client, start_value=1000.0)
    _add_transaction(client, acc, -200.0, "Aluguel")
    data = client.get(f"{BASE}/{acc}").json()
    assert float(data["total_gains"]) == 0.0
    assert float(data["total_expenses"]) == 200.0
    assert float(data["current_balance"]) == pytest.approx(800.0)


def test_get_balance_mixed_transactions(client):
    acc = _make_account(client, start_value=1000.0)
    _add_transaction(client, acc, 500.0, "Salário")
    _add_transaction(client, acc, -200.0, "Aluguel")
    _add_transaction(client, acc, -50.0, "Supermercado")
    data = client.get(f"{BASE}/{acc}").json()
    assert float(data["total_gains"]) == 500.0
    assert float(data["total_expenses"]) == 250.0
    assert float(data["current_balance"]) == pytest.approx(1250.0)


def test_get_balance_untracked_transactions_excluded(client):
    acc = _make_account(client, start_value=1000.0)
    client.post(TRANSACTIONS_BASE, json={
        "account_id": acc,
        "transaction_date": "2024-01-15",
        "value": -999.0,
        "description": "Não rastreado",
        "type": "debit",
        "tracking": False,
    })
    data = client.get(f"{BASE}/{acc}").json()
    assert float(data["total_expenses"]) == 0.0
    assert float(data["current_balance"]) == pytest.approx(1000.0)


def test_get_balance_not_found(client):
    assert client.get(f"{BASE}/999999").status_code == 404
