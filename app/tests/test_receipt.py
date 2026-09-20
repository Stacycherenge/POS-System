import pytest

def test_create_receipt_success(client):
    new_receipt_data = {
        "receipt_id": 2,
        "sale_id": 2,
        "receipt_number": "REC-2026-0002",
        "issued_date_time": "2026-09-20T20:05:00"
    }
    response = client.post("/receipts/", json=new_receipt_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["receipt_id"] == 2
    assert data["receipt_number"] == "REC-2026-0002"
    assert data["sale_id"] == 2


def test_list_receipts_success(client, test_receipt):
    response = client.get("/receipts/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["receipt_id"] == test_receipt["receipt_id"] for item in data)


def test_get_individual_receipt_success(client, test_receipt):
    rid = test_receipt["receipt_id"]
    response = client.get(f"/receipts/{rid}")
    assert response.status_code == 200
    assert response.json()["receipt_id"] == rid


def test_update_receipt_success(client, test_receipt):
    rid = test_receipt["receipt_id"]
    update_payload = {
        "receipt_number": "REC-2026-0001-REV1",
        "issued_date_time": "2026-09-20T21:00:00"
    }
    
    response = client.put(f"/receipts/{rid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["receipt_number"] == "REC-2026-0001-REV1"
    assert data["issued_date_time"] == "2026-09-20T21:00:00"


def test_delete_receipt_success(client, test_receipt):
    rid = test_receipt["receipt_id"]
    response = client.delete(f"/receipts/{rid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/receipts/{rid}")
    assert get_check.status_code == 404


def test_create_receipt_missing_required_fields(client):
    incomplete_payload = {
        "receipt_id": 3,
        "sale_id": 1
    }
    response = client.post("/receipts/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_receipt_invalid_datatype(client):
    bad_payload = {
        "receipt_id": "NotAnInteger",  
        "sale_id": 1,
        "receipt_number": "REC-9999",
        "issued_date_time": "2026-01-01"
    }
    response = client.post("/receipts/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_receipt_returns_404(client):
    response = client.get("/receipts/99999")
    assert response.status_code == 404


def test_update_nonexistent_receipt_returns_404(client):
    update_payload = {"receipt_number": "REC-GHOST"}
    response = client.put("/receipts/99999", json=update_payload)
    assert response.status_code == 404
