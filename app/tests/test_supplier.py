import pytest


def test_create_supplier_success(client):
    new_supplier_data = {
        "company_name": "Global Logistics Medical",
        "contact_name": "Robert Harrison",
        "phone_number": "+254744444444",
        "email": "orders@globalmed.com",
        "is_active": True
    }
    response = client.post("/suppliers/", json=new_supplier_data)
    assert response.status_code == 201
    
    data = response.json()
    assert "supplier_id" in data
    assert data["company_name"] == "Global Logistics Medical"
    assert "created_at" in data


def test_list_suppliers_success(client, test_supplier):
    response = client.get("/suppliers/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["supplier_id"] == test_supplier["supplier_id"] for item in data)


def test_get_individual_supplier_success(client, test_supplier):
    sup_id = test_supplier["supplier_id"]
    response = client.get(f"/suppliers/{sup_id}")
    assert response.status_code == 200
    assert response.json()["supplier_id"] == sup_id


def test_update_supplier_success(client, test_supplier):
    sup_id = test_supplier["supplier_id"]
    update_payload = {
        "contact_name": "Dr. Alice Smith-Jones",
        "phone_number": "+254799999999"
    }
    
    response = client.put(f"/suppliers/{sup_id}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["contact_name"] == "Dr. Alice Smith-Jones"
    assert data["phone_number"] == "+254799999999"


def test_delete_supplier_success(client, test_supplier):
    sup_id = test_supplier["supplier_id"]
    response = client.delete(f"/suppliers/{sup_id}")
    assert response.status_code == 204
    
    get_check = client.get(f"/suppliers/{sup_id}")
    assert get_check.status_code == 404


def test_create_supplier_missing_required_fields(client):
    incomplete_payload = {
        "contact_name": "Incomplete Supplier Entry",
        "phone_number": "+12345"
    }
    response = client.post("/suppliers/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_supplier_invalid_datatype(client):
    bad_payload = {
        "company_name": "Bad Logistics",
        "contact_name": "John Doe",
        "phone_number": "+111222",
        "email": "test@test.com",
        "is_active": "NotABoolean"  
    }
    response = client.post("/suppliers/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_supplier_returns_404(client):
    response = client.get("/suppliers/99999")
    assert response.status_code == 404


def test_update_nonexistent_supplier_returns_404(client):
    update_payload = {"company_name": "Ghost Distribution"}
    response = client.put("/suppliers/99999", json=update_payload)
    assert response.status_code == 404
