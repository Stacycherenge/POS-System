import pytest


def test_create_sale_item_success(client):
    new_item_data = {
        "sale_item_id": 2,
        "sale_id": 1,
        "product_id": 1001,  
        "quantity_sold": 2,
        "price_at_sale": "15.75"
    }
    response = client.post("/sale-items/", json=new_item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["sale_item_id"] == 2
    assert data["quantity_sold"] == 2
    assert data["price_at_sale"] == "15.75"


def test_list_sale_items_success(client, test_sale_item):
    response = client.get("/sale-items/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["sale_item_id"] == test_sale_item["sale_item_id"] for item in data)


def test_get_individual_sale_item_success(client, test_sale_item):
    si_id = test_sale_item["sale_item_id"]
    response = client.get(f"/sale-items/{si_id}")
    assert response.status_code == 200
    assert response.json()["sale_item_id"] == si_id


def test_update_sale_item_success(client, test_sale_item):
    si_id = test_sale_item["sale_item_id"]
    update_payload = {
        "quantity_sold": 12,
        "price_at_sale": "85.00"
    }
    
    response = client.put(f"/sale-items/{si_id}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["quantity_sold"] == 12
    assert data["price_at_sale"] == "85.00"


def test_delete_sale_item_success(client, test_sale_item):
    si_id = test_sale_item["sale_item_id"]
    response = client.delete(f"/sale-items/{si_id}")
    assert response.status_code == 204
    
    get_check = client.get(f"/sale-items/{si_id}")
    assert get_check.status_code == 404


def test_create_sale_item_missing_required_fields(client):
    incomplete_payload = {
        "sale_item_id": 3,
        "sale_id": 1
    }
    response = client.post("/sale-items/", json=incomplete_payload)
    assert response.status_code == 422


def test_create_sale_item_invalid_datatype(client):
    bad_payload = {
        "sale_item_id": "NotAnInteger",  
        "sale_id": 1,
        "product_id": 1001,
        "quantity_sold": "ThreeItems",   
        "price_at_sale": "Free"          
    }
    response = client.post("/sale-items/", json=bad_payload)
    assert response.status_code == 422


def test_get_nonexistent_sale_item_returns_404(client):
    response = client.get("/sale-items/99999")
    assert response.status_code == 404


def test_update_nonexistent_sale_item_returns_404(client):
    update_payload = {"quantity_sold": 100}
    response = client.put("/sale-items/99999", json=update_payload)
    assert response.status_code == 404
