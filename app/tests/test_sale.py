import pytest


def test_create_sale_success(client, test_user, test_customer):
    new_sale_data = {
        "sale_id": 2,
        "user_id": test_user["user_id"],
        "customer_id": test_customer["customer_id"],
        "sale_date_time": "2026-09-20T21:25:00",
        "total_amount": "55.00",
        "sub_total": "50.00",
        "tax_amount": "5.00",
        "is_active": True
    }
    response = client.post("/sales/", json=new_sale_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["sale_id"] == 2
    assert data["total_amount"] == "55.00"
    assert data["tax_amount"] == "5.00"


def test_list_sales_success(client, test_sale):
    response = client.get("/sales/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["sale_id"] == test_sale["sale_id"] for item in data)


def test_get_individual_sale_success(client, test_sale):
    sid = test_sale["sale_id"]
    response = client.get(f"/sales/{sid}")
    assert response.status_code == 200
    assert response.json()["sale_id"] == sid


def test_update_sale_success(client, test_sale):
    sid = test_sale["sale_id"]
    update_payload = {
        "total_amount": "130.00",
        "sub_total": "110.00"
    }
    
    response = client.put(f"/sales/{sid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_amount"] == "130.00"
    assert data["sub_total"] == "110.00"


def test_delete_sale_success(client, test_sale):
    sid = test_sale["sale_id"]
    response = client.delete(f"/sales/{sid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/sales/{sid}")
    assert get_check.status_code == 404


def test_create_sale_missing_required_fields(client):
    incomplete_payload = {
        "sale_id": 3,
        "user_id": 1,
        "sale_date_time": "2026-09-20T21:00:00"
        # Missing total_amount, sub_total, tax_amount
    }
    response = client.post("/sales/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_sale_invalid_datatype(client):
    bad_payload = {
        "sale_id": "NotAnInteger",  
        "user_id": 1,
        "sale_date_time": "2026-01-01",
        "total_amount": "FreeOfCharge", 
        "sub_total": "0.00",
        "tax_amount": "0.00"
    }
    response = client.post("/sales/", json=bad_payload)
    assert response.status_code == 422



def test_get_nonexistent_sale_returns_404(client):
    response = client.get("/sales/99999")
    assert response.status_code == 404


def test_update_nonexistent_sale_returns_404(client):
    update_payload = {"total_amount": "10.00"}
    response = client.put("/sales/99999", json=update_payload)
    assert response.status_code == 404
