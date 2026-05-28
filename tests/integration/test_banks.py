BASE = "/api/v1/banks"


def test_list_banks_returns_seeded_data(client):
    resp = client.get(BASE)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "bank_id" in data[0]
    assert "bank_name" in data[0]


def test_list_banks_pagination(client):
    resp = client.get(f"{BASE}?skip=0&limit=3")
    assert resp.status_code == 200
    assert len(resp.json()) <= 3


def test_get_bank_by_id(client):
    banks = client.get(BASE).json()
    bank_id = banks[0]["bank_id"]

    resp = client.get(f"{BASE}/{bank_id}")
    assert resp.status_code == 200
    assert resp.json()["bank_id"] == bank_id
    assert "bank_name" in resp.json()


def test_get_bank_not_found(client):
    resp = client.get(f"{BASE}/999999")
    assert resp.status_code == 404
