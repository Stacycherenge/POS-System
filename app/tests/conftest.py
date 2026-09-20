import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from database import Base, get_db
from main import app
engine = create_engine(
    "sqlite:///:memory:",  
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(name="client")
def client_fixture():
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    test_user_data = {
        "username": "testuser",
        "email": "test@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "password": "testpassword",
        "user_id": 1, 
        "is_active": True
    }
    
    response = client.post("/auth/register", json=test_user_data)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_user setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return test_user_data


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    
    if response.status_code != 200:
        raise RuntimeError(f"Login failed! Status: {response.status_code}, Body: {response.text}")
        
    token_data = response.json()
    access_token = token_data["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}



@pytest.fixture
def valid_product_payload():
    return {
        "product_id": 1001,
        "name": "Amoxicillin",
        "brand": "Sandoz",
        "product_price": 15.75,
        "stock_quantity": 150,
        "expiry_date": "2028-06-30",
        "is_prescription_required": True,
        "product_form": "capsule",
        "category_id": 1,
        "supplier_id": 1,
        "is_active": True
    }

@pytest.fixture
def test_category(client):
    category_payload = {
        "category_id": 1,  
        "category_name": "Pharmaceuticals",
        "description": "Medicines, tablets, and prescription drugs",
        "is_active": True
    }
    
    response = client.post("/categories/", json=category_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_category setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return category_payload

@pytest.fixture
def test_customer(client, test_user):
    customer_payload = {
        "customer_id": 1,
        "user_id": test_user["user_id"],  
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+254700000000",
        "date_of_birth": "1995-05-15",
        "is_active": True
    }
    
    response = client.post("/customers/", json=customer_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_customer setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return customer_payload


@pytest.fixture
def test_payment(client):
    payment_payload = {
        "payment_id": 1,
        "sale_id": 1,         
        "payment_method": "M-Pesa",
        "amount_paid": "1500.00" 
    }
    
    response = client.post("/payments/", json=payment_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_payment setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return payment_payload

@pytest.fixture
def test_receipt(client):
    receipt_payload = {
        "receipt_id": 1,
        "sale_id": 1,
        "receipt_number": "REC-2026-0001",
        "issued_date_time": "2026-09-20T20:00:00"
    }
    
    response = client.post("/receipts/", json=receipt_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_receipt setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return receipt_payload


@pytest.fixture
def test_sale_item(client, auth_headers):
    product_payload = {
        "product_id": 1001,
        "name": "Amoxicillin",
        "brand": "Sandoz",
        "product_price": "15.75",  
        "stock_quantity": 150,
        "expiry_date": "2028-06-30",
        "is_prescription_required": True,
        "product_form": "capsule",
        "category_id": 1,
        "supplier_id": 1,
        "is_active": True
    }
    client.post("/products/", json=product_payload, headers=auth_headers)

    sale_payload = {
        "sale_id": 1,
        "customer_id": 1,
        "user_id": 1,
        "total_amount": "78.75",
        "status": "completed"
    }
    client.post("/sales/", json=sale_payload, headers=auth_headers) 

    sale_item_payload = {
        "sale_item_id": 1,
        "sale_id": 1,                               
        "product_id": 1001,   
        "quantity_sold": 5,
        "price_at_sale": "78.75"                    
    }
    
    response = client.post("/sale-items/", json=sale_item_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_sale_item setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return sale_item_payload

@pytest.fixture
def test_sale(client, test_user, test_customer):
    sale_payload = {
        "sale_id": 1,
        "user_id": test_user["user_id"],
        "customer_id": test_customer["customer_id"],
        "sale_date_time": "2026-09-20T21:20:00",
        "total_amount": "120.50",
        "sub_total": "100.00",
        "tax_amount": "20.50",
        "is_active": True
    }
    
    response = client.post("/sales/", json=sale_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_sale setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return sale_payload

@pytest.fixture
def test_supplier(client):
    supplier_payload = {
        "company_name": "PharmaCo Industries",
        "contact_name": "Dr. Alice Smith",
        "phone_number": "+254733333333",
        "email": "supply@pharmaco.com",
        "is_active": True
    }
    
    response = client.post("/suppliers/", json=supplier_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"test_supplier setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return response.json() 

@pytest.fixture
def another_test_user(client):
    user_payload = {
        "username": "secondary_worker",
        "email": "secondary@pharmacy.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "role": "pharmacist",
        "password": "securepassword123",
        "is_active": True
    }
    
    response = client.post("/users/", json=user_payload)
    
    if response.status_code != 201:
        raise RuntimeError(f"another_test_user setup failed! Status: {response.status_code}, Body: {response.text}")
        
    return response.json()