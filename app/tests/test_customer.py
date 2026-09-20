import pytest

def test_create_customer_success(client, test_user):
    new_customer_data = {
        "customer_id": 2,
        "user_id": test_user["user_id"],
        "first_name": "Jane",
        "last_name": "Smith",
        "phone_number": "+254711111111",
        "date_of_birth": "1998-11-23",
        "is_active": True
    }
    response = client.post("/customers/", json=new_customer_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["customer_id"] == 2
    assert data["first_name"] == "Jane"
    assert data["user_id"] == test_user["user_id"]
    assert "created_at" in data


def test_list_customers_success(client, test_customer):
    response = client.get("/customers/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["customer_id"] == test_customer["customer_id"] for item in data)


def test_get_individual_customer_success(client, test_customer):
    cid = test_customer["customer_id"]
    response = client.get(f"/customers/{cid}")
    assert response.status_code == 200
    assert response.json()["customer_id"] == cid


def test_update_customer_success(client, test_customer):
    cid = test_customer["customer_id"]
    update_payload = {
        "first_name": "Johnathan",
        "phone_number": "+254722222222"
    }
    
    response = client.put(f"/customers/{cid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["first_name"] == "Johnathan"
    assert data["phone_number"] == "+254722222222"


def test_delete_customer_success(client, test_customer):
    cid = test_customer["customer_id"]
    response = client.delete(f"/customers/{cid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/customers/{cid}")
    assert get_check.status_code == 404


def test_create_customer_missing_required_fields(client):
    incomplete_payload = {
        "customer_id": 3,
        "user_id": 1,
        "first_name": "Incomplete"
    }
    response = client.post("/customers/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_customer_invalid_datatype(client):
    bad_payload = {
        "customer_id": "NotAnInteger",  
        "user_id": 1,
        "first_name": "Jane",
        "last_name": "Doe",
        "phone_number": "+254711111111",
        "date_of_birth": "1995-01-01"
    }
    response = client.post("/customers/", json=bad_payload)
    assert response.status_code == 422

def test_get_nonexistent_customer_returns_404(client):
    response = client.get("/customers/99999")
    assert response.status_code == 404


def test_update_nonexistent_customer_returns_404(client):
    update_payload = {"first_name": "Ghost Customer"}
    response = client.put("/customers/99999", json=update_payload)
    assert response.status_code == 404
