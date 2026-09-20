import pytest


def test_create_category_success(client):
    new_category_data = {
        "category_id": 2,  
        "category_name": "Medical Equipment",
        "description": "Surgical tools and devices",
        "is_active": True
    }
    response = client.post("/categories/", json=new_category_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["category_id"] == 2
    assert data["category_name"] == "Medical Equipment"
    assert "created_at" in data


def test_list_categories_success(client, test_category):
    response = client.get("/categories/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["category_id"] == test_category["category_id"] for item in data)


def test_get_individual_category_success(client, test_category):
    cid = test_category["category_id"]
    response = client.get(f"/categories/{cid}")
    assert response.status_code == 200
    assert response.json()["category_id"] == cid


def test_update_category_success(client, test_category):
    cid = test_category["category_id"]
    update_payload = {
        "category_name": "Pharmaceuticals & Drugs",
        "description": "Updated medicine description"
    }
    
    response = client.put(f"/categories/{cid}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["category_name"] == "Pharmaceuticals & Drugs"
    assert data["description"] == "Updated medicine description"


def test_delete_category_success(client, test_category):
    cid = test_category["category_id"]
    response = client.delete(f"/categories/{cid}")
    assert response.status_code == 204
    
    get_check = client.get(f"/categories/{cid}")
    assert get_check.status_code == 404



def test_create_category_missing_required_fields(client):
    incomplete_payload = {
        "category_id": 3,
        "description": "Missing a category name"
    }
    response = client.post("/categories/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_category_invalid_types(client):
    bad_payload = {
        "category_id": "NotAnInteger",  
        "category_name": 12345,
        "is_active": "NotABoolean"
    }
    response = client.post("/categories/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_category_returns_404(client):
    response = client.get("/categories/99999")
    assert response.status_code == 404


def test_update_nonexistent_category_returns_404(client):
    update_payload = {"category_name": "Ghost Category"}
    response = client.put("/categories/99999", json=update_payload)
    assert response.status_code == 404
