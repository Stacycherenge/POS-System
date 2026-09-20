import pytest


def test_create_payment_success(client):
    new_payment_data = {
        "payment_id": 2,
        "sale_id": 2,
        "payment_method": "Cash",
        "amount_paid": "250.50"
    }
    response = client.post("/payments/", json=new_payment_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["payment_id"] == 2
    assert data["payment_method"] == "Cash"
    assert data["amount_paid"] == "250.50"


def test_list_payments_success(client, test_payment):
    response = client.get("/payments/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["payment_id"] == test_payment["payment_id"] for item in data)


def test_get_individual_payment_success(client, test_payment):
    pid = test_payment["payment_id"]
    response = client.get(f"/payments/{pid}")
    assert response.status_code == 200
    assert response.json()["payment_id"] == pid


def test_update_payment_success(client, test_payment):
    pid = test_payment["payment_id"]
    update_payload = {
        "payment_method": "Credit Card",
        "amount_paid": "1650.00"
    }
    
    response = client.put(f"/payments/{pid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["payment_method"] == "Credit Card"
    assert data["amount_paid"] == "1650.00"


def test_delete_payment_success(client, test_payment):
    pid = test_payment["payment_id"]
    response = client.delete(f"/payments/{pid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/payments/{pid}")
    assert get_check.status_code == 404


def test_create_payment_missing_required_fields(client):
    incomplete_payload = {
        "payment_id": 3,
        "amount_paid": "500.00"
    }
    response = client.post("/payments/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_payment_invalid_datatype(client):
    bad_payload = {
        "payment_id": "NotAnInteger",  
        "sale_id": 1,
        "payment_method": "Cash",
        "amount_paid": "LotsOfMoney"   
    }
    response = client.post("/payments/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_payment_returns_404(client):
    response = client.get("/payments/99999")
    assert response.status_code == 404


def test_update_nonexistent_payment_returns_404(client):
    update_payload = {"payment_method": "Visa"}
    response = client.put("/payments/99999", json=update_payload)
    assert response.status_code == 404
