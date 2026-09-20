import pytest

def test_create_product_success(client, auth_headers, valid_product_payload):
    response = client.post("/products/", json=valid_product_payload, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["product_id"] == valid_product_payload["product_id"]
    assert data["name"] == valid_product_payload["name"]
    assert data["product_price"] == "15.75"
    assert "created_at" in data


def test_list_products_success(client, auth_headers, valid_product_payload):
    client.post("/products/", json=valid_product_payload, headers=auth_headers)
    
    response = client.get("/products/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(item["product_id"] == valid_product_payload["product_id"] for item in data)


def test_get_individual_product_success(client, auth_headers, valid_product_payload):
    client.post("/products/", json=valid_product_payload, headers=auth_headers)
    
    pid = valid_product_payload["product_id"]
    response = client.get(f"/products/{pid}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["product_id"] == pid


def test_update_product_success(client, auth_headers, valid_product_payload):
    client.post("/products/", json=valid_product_payload, headers=auth_headers)
    
    pid = valid_product_payload["product_id"]
    update_payload = {
        "name": "Amoxicillin Enhanced",
        "stock_quantity": 225,
        "product_price": 18.50
    }
    
    response = client.put(f"/products/{pid}", json=update_payload, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Amoxicillin Enhanced"
    assert data["stock_quantity"] == 225
    assert data["product_price"] == "18.50"


def test_delete_product_success(client, auth_headers, valid_product_payload):
    client.post("/products/", json=valid_product_payload, headers=auth_headers)
    
    pid = valid_product_payload["product_id"]
    response = client.delete(f"/products/{pid}", headers=auth_headers)
    assert response.status_code == 204
    
    get_check = client.get(f"/products/{pid}", headers=auth_headers)
    assert get_check.status_code == 404


@pytest.mark.parametrize("missing_field", [
    "name", "brand", "product_price", "stock_quantity", "expiry_date", "product_form"
])
def test_create_product_missing_required_fields(client, auth_headers, valid_product_payload, missing_field):
    payload = valid_product_payload.copy()
    del payload[missing_field]
    
    response = client.post("/products/", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_create_product_datatype_mismatch(client, auth_headers, valid_product_payload):
    payload = valid_product_payload.copy()
    payload["stock_quantity"] = "NotANumber"
    
    response = client.post("/products/", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_get_nonexistent_product_returns_404(client, auth_headers):
    response = client.get("/products/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_nonexistent_product_returns_404(client, auth_headers):
    patch_data = {"name": "Ghost Medicine"}
    response = client.put("/products/99999", json=patch_data, headers=auth_headers)
    assert response.status_code == 404
    
def test_product_endpoints_unauthorized(client, valid_product_payload):
    assert client.get("/products/").status_code == 401
    assert client.get("/products/1001").status_code == 401
    assert client.post("/products/", json=valid_product_payload).status_code == 401
