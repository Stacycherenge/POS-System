import pytest


def test_create_user_success(client):
    new_user_payload = {
        "username": "cashier_john",
        "email": "john.doe@pharmacy.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "cashier",
        "password": "johnspassword456",
        "is_active": True
    }
    response = client.post("/users/", json=new_user_payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "user_id" in data
    assert data["username"] == "cashier_john"
    assert data["email"] == "john.doe@pharmacy.com"
    assert "created_at" in data


def test_list_users_success(client, another_test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["user_id"] == another_test_user["user_id"] for item in data)


def test_get_individual_user_success(client, another_test_user):
    uid = another_test_user["user_id"]
    response = client.get(f"/users/{uid}")
    assert response.status_code == 200
    assert response.json()["user_id"] == uid


def test_update_user_success(client, another_test_user):
    uid = another_test_user["user_id"]
    update_payload = {
        "first_name": "Janet",
        "role": "manager"
    }
    
    response = client.put(f"/users/{uid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["first_name"] == "Janet"
    assert data["role"] == "manager"


def test_delete_user_success(client, another_test_user):
    uid = another_test_user["user_id"]
    response = client.delete(f"/users/{uid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/users/{uid}")
    assert get_check.status_code == 404


def test_create_user_missing_required_fields(client):
    incomplete_payload = {
        "username": "incomplete_user",
        "email": "missing_fields@test.com"
    }
    response = client.post("/users/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_user_invalid_datatype(client):
    bad_payload = {
        "username": "faulty_types",
        "email": "faulty@test.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "cashier",
        "password": "password123",
        "is_active": "NotABoolean"  
    }
    response = client.post("/users/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_user_returns_404(client):
    response = client.get("/users/99999")
    assert response.status_code == 404


def test_update_nonexistent_user_returns_404(client):
    update_payload = {"first_name": "Ghost Name"}
    response = client.put("/users/99999", json=update_payload)
    assert response.status_code == 404
